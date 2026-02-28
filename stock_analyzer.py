#!/usr/bin/env python3
"""
Beurs Cowboy - Main Application

ETL Pipeline: Extract → Transform → Load/Analyze
"""

import logging
from datetime import datetime, date
from typing import Dict, List, Any, Optional, Tuple

from config import (
    SENTIMENT_KEYWORDS, MACRO_KEYWORDS, RSS_FEEDS, REGIONAL_FEEDS,
    TECHNICAL_PARAMS, SCORING_WEIGHTS, TICKERS, COMPANY_NAMES, SECTORS,
    SETTINGS
)
from extractors import (
    fetch_rss_news, fetch_stocktwits_trending, fetch_ticker_data,
    get_all_tickers
)
from transformers import (
    calculate_technical_indicators, calculate_setup_score,
    calculate_potential_upside, get_trade_setup_type, get_signal
)
from analyzers import (
    analyze_sentiment_batch, analyze_regional_sentiment,
    get_keyword_sentiment
)
from loaders import (
    generate_main_site, generate_article, generate_watchlist,
    generate_archive, save_snapshot, generate_search_data
)
from ticker_pages import generate_ticker_pages

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MarketAnalyzer:
    """
    Main market analysis orchestrator.
    Implements ETL pattern voor beursanalyse.
    """
    
    def __init__(self):
        self.output_dir = SETTINGS['output_dir']
        self.data_dir = SETTINGS['data_dir']
        self.results: List[Dict[str, Any]] = []
        self.snapshot_data: Dict[str, Any] = {}
        self.regional_sentiment: Dict[str, Any] = {}
        
    def run(self) -> None:
        """Execute complete ETL pipeline"""
        today = date.today()
        today_str = today.strftime("%Y-%m-%d")
        
        logger.info(f"📈 Market Analysis - {today_str}")
        logger.info("=" * 50)
        
        # EXTRACT: Verzamel ruwe data
        logger.info("\n📥 EXTRACT PHASE")
        market_news, regional_news = self._extract_news()  # Fetch news FIRST
        ticker_data, ticker_headlines = self._extract_ticker_data(market_news)  # Pass news
        trending_symbols = self._extract_social_sentiment()
        
        # TRANSFORM: Verwerk en verrijk data
        logger.info("\n🔄 TRANSFORM PHASE")
        self.regional_sentiment = self._transform_regional_sentiment(regional_news)
        
        # ANALYZE: Sentiment analyse
        logger.info("\n🤖 ANALYZE PHASE")
        sentiments = self._analyze_sentiments(ticker_headlines)
        
        # LOAD: Verwerk resultaten en genereer output
        logger.info("\n📊 LOAD PHASE")
        self._load_analysis_results(
            ticker_data, sentiments, trending_symbols
        )
        
        # GENERATE: Creëer output bestanden
        logger.info(f"\n📝 GENERATE PHASE")
        self._generate_outputs(today, today_str)
        
        logger.info(f"\n✅ Analysis complete - Output in {self.output_dir}/")
    
    def _extract_ticker_data(self, market_news: List[Dict] = None) -> Tuple[Dict, Dict]:
        """Extract: Haal ticker data en headlines op"""
        logger.info("  Fetching ticker data...")
        
        # Get all tickers (base + discovered)
        tickers = get_all_tickers()
        logger.info(f"  Analyzing {len(tickers)} tickers (base: {len(TICKERS)}, discovered: {len(tickers) - len(TICKERS)})")
        
        return fetch_ticker_data(tickers, SETTINGS['max_headlines_per_ticker'], market_news)
    
    def _extract_news(self) -> Tuple[List[Dict], Dict[str, List[Dict]]]:
        """Extract: Haal RSS nieuws op"""
        logger.info("  Fetching RSS news...")
        return fetch_rss_news(
            max_age_hours=SETTINGS['max_age_hours'],
            feed_limit=SETTINGS['rss_feed_limit'],
            workers=SETTINGS['parallel_workers']
        )
    
    def _extract_social_sentiment(self) -> Dict[str, Any]:
        """Extract: Haal social media sentiment op"""
        logger.info("  Fetching social sentiment...")
        return fetch_stocktwits_trending(limit=10)
    
    def _transform_regional_sentiment(self, regional_news: Dict) -> Dict:
        """Transform: Bereken regionaal sentiment"""
        logger.info("  Calculating regional sentiment...")
        sentiment = analyze_regional_sentiment(regional_news, MACRO_KEYWORDS)
        
        # Display results
        for region, data in sorted(sentiment.items(), key=lambda x: x[1]['score'], reverse=True):
            if data['articles_count'] > 0:
                emoji = "🟢" if data['sentiment'] == 'Positief' else "🔴" if data['sentiment'] == 'Negatief' else "⚪"
                logger.info(f"  {emoji} {region}: {data['sentiment']} (score: {data['score']:+.2f})")
        
        return sentiment
    
    def _analyze_sentiments(self, ticker_headlines: Dict) -> Dict:
        """Analyze: Batch sentiment analyse"""
        return analyze_sentiment_batch(ticker_headlines, SENTIMENT_KEYWORDS)
    
    def _load_analysis_results(
        self,
        ticker_data: Dict,
        sentiments: Dict,
        trending_symbols: Dict
    ) -> None:
        """Load: Verwerk alle data naar eindresultaten"""
        logger.info("  Processing analysis results...")
        
        for ticker, data in ticker_data.items():
            try:
                result = self._process_single_ticker(
                    ticker, data, sentiments, trending_symbols
                )
                if result:
                    self.results.append(result)
                    self.snapshot_data[ticker] = result
                    
                    # Log signal
                    signal = result['signal']
                    emoji = "🟢" if "Koop" in signal else "🔴" if "Verkoop" in signal else "⚪"
                    logger.debug(f"  {emoji} {ticker}: {signal}")
                    
            except Exception as e:
                logger.error(f"  Error processing {ticker}: {e}")
                continue
        
        # Sorteer op setup_score
        self.results.sort(key=lambda x: x['setup_score'], reverse=True)
    
    def _process_single_ticker(
        self,
        ticker: str,
        data: Dict,
        sentiments: Dict,
        trending_symbols: Dict
    ) -> Optional[Dict[str, Any]]:
        """Proces single ticker naar resultaat"""
        hist = data['hist']
        current_price = data['current_price']
        avg_price = data['avg_price']
        
        # Bereken technische indicatoren
        indicators = calculate_technical_indicators(hist, TECHNICAL_PARAMS)
        
        # Haal sentiment op
        sentiment = sentiments.get(
            ticker,
            {"score": 0.0, "summary": "Geen nieuws", "catalyst": "Geen"}
        )
        
        # Voeg StockTwits bonus toe
        if ticker in trending_symbols:
            watchlist_count = trending_symbols[ticker]
            bonus = min(
                watchlist_count / 1_000_000 * SCORING_WEIGHTS['stocktwits_max_bonus'],
                SCORING_WEIGHTS['stocktwits_max_bonus']
            )
            sentiment['score'] += bonus
            sentiment['stocktwits_watchlist'] = watchlist_count
            sentiment['is_trending'] = True
        else:
            sentiment['stocktwits_watchlist'] = None
            sentiment['is_trending'] = False
        
        # Bereken setup score
        setup_score, setup_reasons = calculate_setup_score(
            indicators, current_price, avg_price, SCORING_WEIGHTS
        )
        
        # Totale score
        total_score = setup_score + (sentiment['score'] * SCORING_WEIGHTS['sentiment_multiplier'])
        
        # Bepaal setup type en signaal
        setup_type = get_trade_setup_type(indicators, current_price)
        potential_upside = calculate_potential_upside(indicators, current_price)
        signal, signal_class = get_signal(total_score, potential_upside)
        
        # Prijs verandering
        prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        price_change = ((current_price - prev_close) / prev_close) * 100
        
        return {
            "ticker": ticker,
            "name": COMPANY_NAMES.get(ticker, ticker),
            "sector": SECTORS.get(ticker, 'Overig'),
            "price": round(current_price, 2),
            "change": round(price_change, 2),
            "change_pct": round(price_change, 2),
            "rsi": round(indicators['rsi'], 1),
            "macd": round(indicators['macd'], 4),
            "macd_hist": round(indicators['macd_hist'], 4),
            "sma_20": round(indicators['sma_20'], 2),
            "sma_50": round(indicators['sma_50'], 2) if indicators['sma_50'] else None,
            "atr_pct": round(indicators['atr_pct'], 1),
            "vol_rank": round(indicators['vol_rank'], 0),
            "setup_score": round(total_score, 1),
            "setup_reasons": setup_reasons,
            "setup_type": setup_type,
            "potential_upside": round(potential_upside, 1),
            "sentiment_score": round(sentiment['score'], 2),
            "sentiment_summary": sentiment['summary'],
            "catalyst": sentiment['catalyst'],
            "is_trending": sentiment.get('is_trending', False),
            "stocktwits_watchlist": sentiment.get('stocktwits_watchlist'),
            "signal": signal,
            "signal_class": signal_class,
            "high_52w": round(indicators['high_52w'], 2),
            "low_52w": round(indicators['low_52w'], 2),
            "volume": int(indicators['volume']),
        }
    
    def _generate_outputs(self, today: date, today_str: str) -> None:
        """Generate: Creëer alle output bestanden"""
        trending_stocks = [r for r in self.results if r.get('is_trending')]
        
        generate_main_site(self.results, today, trending_stocks, self.regional_sentiment)
        generate_article(self.results, today)
        generate_watchlist(self.results, today)
        generate_archive(self.results, today, self.data_dir)
        generate_ticker_pages(self.results, self.output_dir)
        save_snapshot(self.snapshot_data, today_str, self.data_dir)
        generate_search_data(self.results, today_str, self.output_dir)
        
        logger.info(f"  ✓ Generated site in {self.output_dir}/")
        logger.info(f"  ✓ Generated {len(self.results)} ticker pages")


def main():
    """Main entry point"""
    analyzer = MarketAnalyzer()
    analyzer.run()


if __name__ == "__main__":
    main()
