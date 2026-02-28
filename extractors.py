"""
Data Extractors

Verantwoordelijk voor het ophalen van ruwe data:
- RSS feeds
- Yahoo Finance
- Social media (StockTwits)
"""

import datetime
import concurrent.futures
import feedparser
import yfinance as yf
import urllib.request
import json
from typing import Dict, List, Tuple, Any, Optional

from config import RSS_FEEDS, REGIONAL_FEEDS, TICKERS, TICKER_DISCOVER, DISCOVER_SETTINGS


def get_all_tickers() -> List[str]:
    """
    Get complete list of tickers dynamically.
    Discovers tickers from multiple sources:
    - Base configuration
    - Yahoo Finance most active
    - Sector ETFs holdings
    - StockTwits trending
    
    Returns:
        Combined list of all discovered tickers
    """
    all_tickers = set(TICKERS)
    
    if not DISCOVER_SETTINGS.get('enabled', True):
        return list(all_tickers)
    
    # Discover from StockTwits trending
    print("  Discovering trending tickers...")
    trending = _discover_stocktwits_trending()
    all_tickers.update(trending)
    
    # Discover from Yahoo Finance most active
    print("  Discovering most active tickers...")
    most_active = _discover_yahoo_most_active()
    all_tickers.update(most_active)
    
    # Add from discovery categories
    for category, tickers in TICKER_DISCOVER.items():
        for ticker in tickers:
            if _validate_ticker(ticker):
                all_tickers.add(ticker)
    
    # Remove duplicates and limit
    result = list(all_tickers)[:DISCOVER_SETTINGS.get('max_tickers', 200)]
    print(f"  ✓ Discovered {len(result)} total tickers")
    
    return result


def _discover_stocktwits_trending(limit: int = 20) -> List[str]:
    """Discover trending tickers from StockTwits"""
    try:
        url = "https://api.stocktwits.com/api/2/trending/symbols.json"
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        trending = []
        for symbol in data.get('symbols', [])[:limit]:
            ticker = symbol.get('symbol', '')
            if ticker and len(ticker) <= 5:  # Filter valid tickers
                trending.append(ticker)
        
        return trending
    except Exception as e:
        print(f"    ⚠️ StockTwits discovery failed: {e}")
        return []


def _discover_yahoo_most_active(limit: int = 20) -> List[str]:
    """Discover most active tickers from Yahoo Finance"""
    try:
        # Get most active stocks
        most_active = yf.MostActive()
        tickers = [stock.symbol for stock in most_active[:limit]]
        return tickers
    except Exception as e:
        print(f"    ⚠️ Yahoo discovery failed: {e}")
        return []


def _validate_ticker(ticker: str) -> bool:
    """
    Quick validation if ticker exists and is tradeable.
    
    Args:
        ticker: Ticker symbol to validate
    
    Returns:
        True if valid, False otherwise
    """
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period='1d')
        
        if hist.empty:
            return False
        
        # Check minimum price and volume
        price = hist['Close'].iloc[-1]
        volume = hist['Volume'].iloc[-1]
        
        min_price = DISCOVER_SETTINGS.get('min_price', 1.0)
        min_volume = DISCOVER_SETTINGS.get('min_volume', 100000)
        
        return price >= min_price and volume >= min_volume
        
    except Exception:
        return False


def fetch_rss_news(
    max_age_hours: int = 24,
    feed_limit: int = 25,
    workers: int = 10
) -> Tuple[List[Dict], Dict[str, List[Dict]]]:
    """
    Fetch RSS news from multiple sources in parallel.
    
    Args:
        max_age_hours: Maximum age of articles in hours
        feed_limit: Max articles per feed
        workers: Number of parallel workers
    
    Returns:
        Tuple of (all_news, regional_news)
    """
    all_news = []
    regional_news = {region: [] for region in REGIONAL_FEEDS.keys()}
    successful_feeds = 0
    failed_feeds = []
    skipped_old = 0

    now_utc = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    cutoff_date = now_utc - datetime.timedelta(hours=max_age_hours)

    # Reverse mapping: feed -> region
    feed_to_region = {}
    for region, feeds in REGIONAL_FEEDS.items():
        for feed in feeds:
            feed_to_region[feed] = region

    def fetch_single_feed(source_url: Tuple[str, str]) -> Tuple[str, List[Dict], Optional[str]]:
        """Fetch a single RSS feed"""
        nonlocal skipped_old
        source, url = source_url
        
        try:
            feed = feedparser.parse(url)
            if not feed.entries:
                return source, [], "No entries"
            
            articles = []
            for entry in feed.entries[:feed_limit]:
                published_date = _parse_date(entry.get('published', ''))
                
                # Check if recent enough
                is_recent = published_date is None or published_date >= cutoff_date
                if is_recent:
                    age_hours = None
                    if published_date:
                        age_hours = (now_utc - published_date).total_seconds() / 3600
                    
                    article = {
                        'source': source,
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.get('published', ''),
                        'summary': entry.get('summary', '')[:500] if entry.get('summary') else '',
                        'is_recent': True,
                        'age_hours': age_hours
                    }
                    articles.append(article)
                    
                    # Add to regional list
                    region = feed_to_region.get(source, 'Overig')
                    if region:
                        regional_news[region].append(article)
                else:
                    skipped_old += 1
            
            return source, articles, None
            
        except Exception as e:
            return source, [], str(e)

    # Fetch feeds in parallel
    feed_results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_source = {
            executor.submit(fetch_single_feed, (source, url)): source
            for source, url in RSS_FEEDS.items()
        }
        for future in concurrent.futures.as_completed(future_to_source):
            source = future_to_source[future]
            try:
                result = future.result()
                feed_results.append(result)
            except Exception as e:
                feed_results.append((source, [], str(e)))
    
    # Process results
    for source, articles, error in feed_results:
        if articles:
            all_news.extend(articles)
            successful_feeds += 1
        else:
            failed_feeds.append(source)

    # Log statistics
    recent_count = sum(1 for n in all_news if n.get('is_recent', False))
    avg_age = sum(n.get('age_hours', 0) or 0 for n in all_news) / len(all_news) if all_news else 0
    
    print(f"  Wereldwijd: {len(all_news)} artikelen ({recent_count} recent, {skipped_old} te oud)")
    print(f"  ✓ {successful_feeds} feeds succes, {len(failed_feeds)} overgeslagen")
    print(f"  ⏱️  Gemiddelde leeftijd: {avg_age:.1f} uur")
    
    return all_news, regional_news


def fetch_ticker_data(
    tickers: List[str],
    max_headlines: int = 10,
    market_news: List[Dict] = None
) -> Tuple[Dict[str, Any], Dict[str, List[str]]]:
    """
    Fetch ticker data and headlines from Yahoo Finance.
    Uses RSS news as fallback for tickers with limited headlines.
    
    Args:
        tickers: List of ticker symbols
        max_headlines: Max headlines per ticker
        market_news: Optional pre-fetched market news for fallback
    
    Returns:
        Tuple of (ticker_data, ticker_headlines)
    """
    ticker_data = {}
    ticker_headlines = {}
    
    # Create ticker-specific news from market news if available
    ticker_news_fallback = {}
    if market_news:
        for article in market_news[:50]:  # Use top 50 market articles
            title = article['title']
            # Try to match tickers in title
            for ticker in tickers:
                if ticker in title or ticker.lower() in title.lower():
                    if ticker not in ticker_news_fallback:
                        ticker_news_fallback[ticker] = []
                    ticker_news_fallback[ticker].append(title)
    
    for ticker in tickers:
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="1y")

            if hist.empty:
                print(f"  {ticker}... ❌")
                continue

            # Get headlines from Yahoo Finance news
            news = t.news
            headlines = []
            
            for n in news:
                title = n.get('title')
                if title:
                    headlines.append(title)
            
            # Supplement with market news if Yahoo has few headlines
            if len(headlines) < max_headlines and ticker in ticker_news_fallback:
                for fb_title in ticker_news_fallback[ticker]:
                    if fb_title not in headlines:
                        headlines.append(f"{ticker}: {fb_title}")
                    if len(headlines) >= max_headlines:
                        break
            
            # Final fallback: general market news
            if len(headlines) < 3 and market_news:
                for article in market_news[:max_headlines - len(headlines)]:
                    headlines.append(f"{ticker} - {article['title']}")
            
            # Last resort fallback
            if not headlines:
                headlines = [f"{ticker} - Markt update vandaag"]
            
            ticker_headlines[ticker] = headlines[:max_headlines]

            ticker_data[ticker] = {
                'hist': hist,
                'current_price': hist['Close'].iloc[-1],
                'avg_price': hist['Close'].mean(),
                'news': news,
                'ticker_obj': t
            }
            print(f"  {ticker}... ✓ {len(headlines)} headlines")

        except Exception as e:
            print(f"  {ticker}... ❌ {e}")
    
    return ticker_data, ticker_headlines


def fetch_stocktwits_trending(limit: int = 10) -> Dict[str, int]:
    """
    Fetch trending symbols from StockTwits.
    
    Args:
        limit: Max trending symbols to fetch
    
    Returns:
        Dict of {symbol: watchlist_count}
    """
    url = "https://api.stocktwits.com/api/2/trending/symbols.json"
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        trending = {}
        for symbol in data.get('symbols', [])[:limit]:
            ticker = symbol.get('symbol', '')
            watchlist_count = symbol.get('watchlist_count', 0)
            if ticker:
                trending[ticker] = watchlist_count
                print(f"  Trending: {ticker} ({watchlist_count:,} watchlist)")
        
        return trending
    
    except Exception as e:
        print(f"  ⚠️ StockTwits error: {e}")
        return {}


def _parse_date(date_str: str) -> Optional[datetime.datetime]:
    """Parse date string to datetime"""
    if not date_str:
        return None
    
    formats = [
        '%a, %d %b %Y %H:%M:%S %Z',
        '%a, %d %b %Y %H:%M:%S GMT',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%d %H:%M:%S'
    ]
    
    for fmt in formats:
        try:
            parsed = datetime.datetime.strptime(date_str, fmt)
            # Make timezone-naive for comparison
            if parsed.tzinfo is not None:
                parsed = parsed.replace(tzinfo=None)
            return parsed
        except (ValueError, TypeError):
            continue
    
    return None
