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

from config import RSS_FEEDS, REGIONAL_FEEDS


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
    max_headlines: int = 10
) -> Tuple[Dict[str, Any], Dict[str, List[str]]]:
    """
    Fetch ticker data and headlines from Yahoo Finance.
    
    Args:
        tickers: List of ticker symbols
        max_headlines: Max headlines per ticker
    
    Returns:
        Tuple of (ticker_data, ticker_headlines)
    """
    ticker_data = {}
    ticker_headlines = {}
    
    for ticker in tickers:
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="1y")

            if hist.empty:
                print(f"  {ticker}... ❌")
                continue

            # Get headlines
            news = t.news
            headlines = [n.get('title') for n in news if n.get('title')]
            
            # Filter by date (last 2 days)
            today = datetime.date.today()
            filtered_headlines = []
            for n in news:
                title = n.get('title')
                if not title:
                    continue
                
                provider_time = n.get('providerPublishTime', 0)
                if provider_time:
                    article_date = datetime.datetime.fromtimestamp(provider_time).date()
                    if article_date >= today - datetime.timedelta(days=1):
                        filtered_headlines.append(title)
                else:
                    filtered_headlines.append(title)
            
            ticker_headlines[ticker] = filtered_headlines[:max_headlines]

            ticker_data[ticker] = {
                'hist': hist,
                'current_price': hist['Close'].iloc[-1],
                'avg_price': hist['Close'].mean(),
                'news': news,
                'ticker_obj': t
            }
            print(f"  {ticker}... ✓ {len(filtered_headlines)} headlines")

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
