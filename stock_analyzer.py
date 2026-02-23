#!/usr/bin/env python3
"""
Beurs Cowboy - Free Stock Analysis Platform

Volledig gratis zonder API keys:
- Yahoo Finance voor data en nieuws (gratis)
- Keyword-based sentiment analyse (geen LLM nodig)
- RSS feeds voor extra nieuws

"Trading is als het wilde westen - er zijn schurken en er zijn sheriffs. Wees een sheriff."
"""

import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import os
import glob
import json
import re
import feedparser

# ============= CONFIGURATION =============
OUTPUT_DIR = "docs"
DATA_DIR = "data_snapshots"
ARCHIVE_DIR = "docs/archive"

TICKERS = [
    # Mega Cap Tech (6)
    'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META',
    # Semiconductors (6)
    'AMD', 'INTC', 'TSM', 'AVGO', 'QCOM', 'TXN',
    # EV & Auto (5)
    'TSLA', 'RIVN', 'LCID', 'F', 'GM',
    # Tech / Software (6)
    'ORCL', 'CRM', 'ADBE', 'NOW', 'INTU', 'PLTR',
    # Social / Media (5)
    'NFLX', 'DIS', 'CMCSA', 'PARA', 'WBD',
    # Finance - Banks (6)
    'JPM', 'BAC', 'GS', 'MS', 'WFC', 'C',
    # Finance - Payments (5)
    'V', 'MA', 'PYPL', 'SQ', 'AFRM',
    # Finance - Crypto (5)
    'COIN', 'MARA', 'RIOT', 'CLSK', 'HUT',
    # Retail (6)
    'WMT', 'TGT', 'COST', 'HD', 'NKE', 'SBUX',
    # Healthcare - Big Pharma (6)
    'JNJ', 'UNH', 'PFE', 'MRNA', 'REGN', 'GILD',
    # Energy (5)
    'XOM', 'CVX', 'COP', 'SLB', 'OXY',
    # Industrials (5)
    'CAT', 'BA', 'GE', 'HON', 'UPS',
    # European (5)
    'ASML.AS', 'SAP', 'NESN.SW', 'NOVN.SW', 'AZN',
    # Cloud / Cybersecurity (6)
    'SNOW', 'NET', 'DDOG', 'ZS', 'CRWD', 'MDB',
    # Biotech (6)
    'BIIB', 'VRTX', 'ALNY', 'BMRN', 'INCY', 'TECH',
    # Real Estate (5)
    'AMT', 'PLD', 'CCI', 'EQIX', 'SPG',
    # Telecom (4)
    'T', 'VZ', 'TMUS', 'CHTR',
    # Consumer Discretionary (6)
    'MCD', 'NKE', 'LULU', 'DECK', 'CROX', 'SKX',
    # Airlines (4)
    'DAL', 'UAL', 'AAL', 'LUV',
    # Cruise Lines (3)
    'CCL', 'RCL', 'NCLH',
    # Gaming (4)
    'DKNG', 'PENN', 'MGM', 'WYNN',
    # Cannabis (4)
    'TLRY', 'SNDL', 'CGC', 'ACB',
    # China Tech (5)
    'BABA', 'JD', 'PDD', 'BIDU', 'NIO',
    # Small Cap Growth (6)
    'UPST', 'SOFI', 'HOOD', 'RBLX', 'U', 'PATH',
    # Dividend Kings (5)
    'KO', 'PEP', 'PG', 'MMM', 'JNJ',
    # Utilities (4)
    'NEE', 'DUK', 'SO', 'D',
    # Materials (4)
    'LIN', 'APD', 'ECL', 'SHW',
    # Defense (4)
    'LMT', 'RTX', 'NOC', 'GD',
]

# ============= FREE SENTIMENT ANALYSIS =============
# Keyword-based sentiment (geen API key nodig!)

POSITIVE_KEYWORDS = [
    'stijgt', 'stijging', 'winst', 'groei', 'record', 'bullish', 'koop',
    'beat', 'outperforms', 'upgrade', 'positive', 'strong', 'growth',
    'surge', 'rally', 'gain', 'profit', 'success', 'breakthrough',
    'optimistic', 'bullish', 'outlook', 'exceeds', 'expectations',
    'koopadvies', 'verwacht', 'positief', 'hoog', 'beter', 'goed',
    'nieuwe', 'lanceert', 'partnership', 'deal', 'contract', 'wint'
]

NEGATIVE_KEYWORDS = [
    'daalt', 'daling', 'verlies', 'crash', 'bearish', 'verkoop',
    'miss', 'underperforms', 'downgrade', 'negative', 'weak', 'decline',
    'drop', 'fall', 'loss', 'failure', 'lawsuit', 'investigation',
    'pessimistic', 'bearish', 'warning', 'below', 'expectations',
    'verkoopadvies', 'risico', 'negatief', 'laag', 'slechter', 'probleem',
    'rechtszaak', 'onderzoek', 'boete', 'terugroep', 'storing', 'fout'
]

# RSS Feeds (gratis)
RSS_FEEDS = {
    'marketwatch': 'https://feeds.marketwatch.com/marketwatch/topstories/',
    'reuters_business': 'https://www.reutersagency.com/feed/',
    'yahoo_finance': 'https://finance.yahoo.com/news/rssindex',
}

# ============= TECHNICAL INDICATORS =============

def calculate_rsi(prices, window=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=window).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(prices, fast=12, slow=26, signal=9):
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line.iloc[-1], signal_line.iloc[-1], histogram.iloc[-1]

def calculate_atr(hist, period=14):
    high = hist['High']
    low = hist['Low']
    close = hist['Close'].shift(1)
    tr1 = high - low
    tr2 = abs(high - close)
    tr3 = abs(low - close)
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(period).mean().iloc[-1]

def get_volatility_rank(hist, period=252):
    if len(hist) < period:
        return 50
    daily_returns = hist['Close'].pct_change()
    current_vol = daily_returns.rolling(20).std().iloc[-1]
    vol_rank = (daily_returns.rolling(20).std() < current_vol).sum() / (period - 20) * 100
    return vol_rank

# ============= FREE SENTIMENT ANALYSIS =============
# Keyword-based sentiment (geen API key nodig!)

def analyze_sentiment(text):
    """
    Eenvoudige keyword-based sentiment analyse.
    Geen API key nodig!
    """
    if not text:
        return 0.0
    
    text_lower = text.lower()
    
    positive_count = sum(1 for keyword in POSITIVE_KEYWORDS if keyword.lower() in text_lower)
    negative_count = sum(1 for keyword in NEGATIVE_KEYWORDS if keyword.lower() in text_lower)
    
    total = positive_count + negative_count
    if total == 0:
        return 0.0
    
    # Score tussen -1.0 en 1.0
    score = (positive_count - negative_count) / total
    return round(score, 2)

def get_sentiment(ticker, headlines):
    """
    Analyseer sentiment van headlines zonder API.
    """
    if not headlines:
        return {"score": 0.0, "summary": "Geen nieuws", "catalyst": "Geen"}
    
    valid_headlines = [h for h in headlines[:5] if h is not None]
    if not valid_headlines:
        return {"score": 0.0, "summary": "Geen nieuws", "catalyst": "Geen"}
    
    # Analyseer elke headline
    scores = []
    summaries = []
    
    for headline in valid_headlines:
        score = analyze_sentiment(headline)
        scores.append(score)
        
        # Bepaal sentiment label
        if score > 0.3:
            summaries.append("Positief")
        elif score < -0.3:
            summaries.append("Negatief")
        else:
            summaries.append("Neutraal")
    
    # Gemiddelde score
    avg_score = sum(scores) / len(scores) if scores else 0.0
    
    # Samenvatting
    if avg_score > 0.3:
        summary = f"Overwegend positief nieuws ({len([s for s in scores if s > 0])}/{len(scores)} positief)"
    elif avg_score < -0.3:
        summary = f"Overwegend negatief nieuws ({len([s for s in scores if s < 0])}/{len(scores)} negatief)"
    else:
        summary = "Gemengd nieuws, geen duidelijke trend"
    
    # Catalyst bepalen
    all_text = " ".join(valid_headlines).lower()
    catalyst = "Geen specifieke catalyst"
    
    if any(k in all_text for k in ['earnings', 'kwartaal', 'resultaat']):
        catalyst = "Komende kwartaalcijfers"
    elif any(k in all_text for k in ['product', 'lanceert', 'nieuwe']):
        catalyst = "Nieuwe productaankondiging"
    elif any(k in all_text for k in ['deal', 'contract', 'partnership']):
        catalyst = "Zakelijke ontwikkeling"
    elif any(k in all_text for k in ['upgrade', 'downgrade', 'advies']):
        catalyst = "Analisten advies wijziging"
    
    return {
        "score": round(avg_score, 2),
        "summary": summary,
        "catalyst": catalyst
    }

def fetch_rss_news():
    """
    Haal nieuws op van gratis RSS feeds.
    """
    all_news = []
    
    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                all_news.append({
                    'source': source,
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.get('published', '')
                })
        except Exception as e:
            pass  # Negeer fouten, we hebben genoeg nieuws van Yahoo
    
    return all_news

# ============= SCORING =============

def calculate_setup_score(rsi, macd_val, macd_signal, macd_hist, current_price, sma_20, sma_50, atr, avg_price):
    score = 0
    reasons = []
    
    if 30 <= rsi <= 40:
        score += 2
        reasons.append("RSI oversold - bounce kans")
    elif 60 <= rsi <= 70:
        score += 1.5
        reasons.append("RSI in bullische zone")
    elif rsi < 30:
        score += 1
        reasons.append("Diep oversold - reversal kans")
    elif rsi > 75:
        score -= 1
        reasons.append("Overbought - correctie risico")
    
    if macd_hist > 0 and macd_val > macd_signal:
        score += 2
        reasons.append("MACD bullisch momentum")
    elif macd_hist < 0 and macd_val < macd_signal:
        score -= 2
        reasons.append("MACD bearish momentum")
    
    if sma_20 and sma_50:
        if current_price > sma_20 > sma_50:
            score += 2
            reasons.append("Bullische MA alignement")
        elif current_price < sma_20 < sma_50:
            score -= 2
            reasons.append("Bearish MA alignement")
        elif abs(current_price - sma_20) / avg_price < 0.02:
            score += 1
            reasons.append("Test 20-daags gemiddelde")
    
    if atr > 0:
        atr_pct = (atr / avg_price) * 100
        if atr_pct > 3:
            score += 1
            reasons.append(f"Hoge volatiliteit (ATR {atr_pct:.1f}%)")
    
    return score, reasons

def calculate_potential_upside(current_price, sma_20, sma_50, high_52w, atr):
    if not sma_20 or not sma_50:
        return 2.0
    
    resistance_to_high = ((high_52w - current_price) / current_price) * 100 if high_52w else 10
    expected_move = (atr / current_price) * 100 if atr else 2
    
    if current_price > sma_20 > sma_50:
        return min(expected_move * 1.5, resistance_to_high)
    if current_price < sma_20 and current_price > sma_50:
        return min(abs(((sma_20 - current_price) / current_price) * 100), expected_move)
    if current_price < sma_50:
        return min(abs(((sma_50 - current_price) / current_price) * 100), expected_move * 1.2)
    
    return expected_move

def get_trade_setup_type(rsi, macd_hist, current_price, sma_20, sma_50):
    if rsi < 30 and macd_hist > 0:
        return "Oversold Reversal"
    elif rsi > 70 and macd_hist < 0:
        return "Overbought Correctie"
    elif current_price > sma_20 > sma_50 and macd_hist > 0:
        return "Trend Volgt"
    elif current_price < sma_20 < sma_50 and macd_hist < 0:
        return "Downtrend Volgt"
    elif abs(current_price - sma_20) / sma_20 < 0.01:
        return "MA Test"
    elif 45 < rsi < 55:
        return "Consolidatie"
    else:
        return "Gemengd Signaal"

def get_signal(score, upside):
    if score >= 4 and upside >= 5:
        return "Sterk Koop", "buy-strong"
    elif score >= 2 and upside >= 4:
        return "Koop", "buy"
    elif score >= 0:
        return "Neutraal", "neutral"
    elif score >= -2:
        return "Voorzichtig", "sell"
    else:
        return "Verkoop", "sell-strong"

# ============= MAIN ANALYSIS =============

def analyze():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    
    print(f"\n📈 Market Analysis - {today_str}")
    print("=" * 50)
    
    results = []
    snapshot_data = {}

    for ticker in TICKERS:
        print(f"  {ticker}...", end=" ")
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="1y")
            
            if hist.empty:
                print("❌")
                continue

            current_price = hist['Close'].iloc[-1]
            avg_price = hist['Close'].mean()
            
            rsi = calculate_rsi(hist['Close']).iloc[-1]
            macd_val, macd_signal, macd_hist = calculate_macd(hist['Close'])
            sma_20 = hist['Close'].rolling(20).mean().iloc[-1]
            sma_50 = hist['Close'].rolling(50).mean().iloc[-1] if len(hist) >= 50 else None
            atr = calculate_atr(hist)
            vol_rank = get_volatility_rank(hist)
            high_52w = hist['High'].max()
            low_52w = hist['Low'].min()
            
            news = t.news
            sentiment = get_sentiment(ticker, [n.get('title') for n in news])
            
            setup_score, setup_reasons = calculate_setup_score(
                rsi, macd_val, macd_signal, macd_hist,
                current_price, sma_20, sma_50, atr, avg_price
            )
            
            total_score = setup_score + (sentiment['score'] * 3)
            potential_upside = calculate_potential_upside(current_price, sma_20, sma_50, high_52w, atr)
            setup_type = get_trade_setup_type(rsi, macd_hist, current_price, sma_20, sma_50)
            signal, signal_class = get_signal(total_score, potential_upside)
            
            # Price change calculation
            prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            price_change = ((current_price - prev_close) / prev_close) * 100
            
            res = {
                "ticker": ticker,
                "name": get_company_name(ticker),
                "sector": get_sector(ticker),
                "price": round(current_price, 2),
                "change": round(price_change, 2),
                "change_pct": round(price_change, 2),
                "rsi": round(rsi, 1),
                "macd": round(macd_val, 4),
                "macd_hist": round(macd_hist, 4),
                "sma_20": round(sma_20, 2),
                "sma_50": round(sma_50, 2) if sma_50 else None,
                "atr_pct": round((atr / current_price) * 100, 1),
                "vol_rank": round(vol_rank, 0),
                "setup_score": round(total_score, 1),
                "setup_reasons": setup_reasons,
                "setup_type": setup_type,
                "potential_upside": round(potential_upside, 1),
                "sentiment_score": round(sentiment['score'], 2),
                "sentiment_summary": sentiment['summary'],
                "catalyst": sentiment['catalyst'],
                "signal": signal,
                "signal_class": signal_class,
                "high_52w": round(high_52w, 2),
                "low_52w": round(low_52w, 2),
                "volume": int(hist['Volume'].iloc[-1])
            }
            results.append(res)
            snapshot_data[ticker] = res
            
            signal_emoji = "🟢" if "Koop" in signal else "🔴" if "Verkoop" in signal or "Voorzichtig" in signal else "⚪"
            print(f"{signal_emoji} {signal}")
            
        except Exception as e:
            print(f"❌ {e}")

    results.sort(key=lambda x: x['setup_score'], reverse=True)
    
    print(f"\n📝 Generating site...")
    generate_main_site(results, today)
    generate_article(results, today)
    save_snapshot(snapshot_data, today_str)
    generate_search_data(results, today_str)
    
    print(f"\n✅ Site generated in {OUTPUT_DIR}/")

def get_company_name(ticker):
    names = {
        'AAPL': 'Apple Inc', 'MSFT': 'Microsoft Corporation', 'NVDA': 'NVIDIA Corporation',
        'GOOGL': 'Alphabet Inc', 'AMZN': 'Amazon.com Inc', 'META': 'Meta Platforms',
        'AMD': 'Advanced Micro Devices', 'INTC': 'Intel Corporation', 'TSM': 'TSMC',
        'AVGO': 'Broadcom Inc', 'QCOM': 'Qualcomm Inc', 'TXN': 'Texas Instruments',
        'TSLA': 'Tesla Inc', 'RIVN': 'Rivian Automotive', 'LCID': 'Lucid Group',
        'F': 'Ford Motor', 'GM': 'General Motors',
        'ORCL': 'Oracle Corporation', 'CRM': 'Salesforce Inc', 'ADBE': 'Adobe Inc',
        'NOW': 'ServiceNow Inc', 'INTU': 'Intuit Inc', 'PLTR': 'Palantir Technologies',
        'NFLX': 'Netflix Inc', 'DIS': 'Walt Disney Co', 'CMCSA': 'Comcast Corp',
        'PARA': 'Paramount Global', 'WBD': 'Warner Bros Discovery',
        'JPM': 'JPMorgan Chase', 'BAC': 'Bank of America', 'GS': 'Goldman Sachs',
        'MS': 'Morgan Stanley', 'WFC': 'Wells Fargo', 'C': 'Citigroup',
        'COIN': 'Coinbase Global', 'MARA': 'Marathon Digital', 'RIOT': 'Riot Platforms',
        'CLSK': 'CleanSpark Inc', 'HUT': 'Hut 8 Mining',
        'V': 'Visa Inc', 'MA': 'Mastercard Inc', 'PYPL': 'PayPal Holdings',
        'SQ': 'Block Inc', 'AFRM': 'Affirm Holdings',
        'WMT': 'Walmart Inc', 'TGT': 'Target Corporation', 'COST': 'Costco Wholesale',
        'HD': 'Home Depot', 'NKE': 'Nike Inc', 'SBUX': 'Starbucks Corporation',
        'JNJ': 'Johnson & Johnson', 'UNH': 'UnitedHealth Group', 'PFE': 'Pfizer Inc',
        'MRNA': 'Moderna Inc', 'REGN': 'Regeneron Pharma', 'GILD': 'Gilead Sciences',
        'XOM': 'Exxon Mobil', 'CVX': 'Chevron Corporation', 'COP': 'ConocoPhillips',
        'SLB': 'Schlumberger Ltd', 'OXY': 'Occidental Petroleum',
        'CAT': 'Caterpillar Inc', 'BA': 'Boeing Company', 'GE': 'General Electric',
        'HON': 'Honeywell International', 'UPS': 'United Parcel Service',
        'ASML.AS': 'ASML Holding', 'SAP': 'SAP SE', 'NESN.SW': 'Nestle SA',
        'NOVN.SW': 'Novartis AG', 'AZN': 'AstraZeneca',
        'SNOW': 'Snowflake Inc', 'NET': 'Cloudflare Inc', 'DDOG': 'Datadog Inc',
        'ZS': 'Zscaler Inc', 'CRWD': 'CrowdStrike Holdings', 'MDB': 'MongoDB Inc',
        'BIIB': 'Biogen Inc', 'VRTX': 'Vertex Pharma', 'ALNY': 'Alnylam Pharma',
        'BMRN': 'BioMarin Pharma', 'INCY': 'Incyte Corp', 'TECH': 'Bio-Techne',
        'AMT': 'American Tower', 'PLD': 'Prologis Inc', 'CCI': 'Crown Castle',
        'EQIX': 'Equinix Inc', 'SPG': 'Simon Property',
        'T': 'AT&T Inc', 'VZ': 'Verizon Comm', 'TMUS': 'T-Mobile US', 'CHTR': 'Charter Comm',
        'MCD': "McDonald's Corp", 'LULU': 'Lululemon Athletica', 'DECK': 'Deckers Outdoor',
        'CROX': 'Crocs Inc', 'SKX': 'Skechers USA',
        'DAL': 'Delta Air Lines', 'UAL': 'United Airlines', 'AAL': 'American Airlines',
        'LUV': 'Southwest Airlines',
        'CCL': 'Carnival Corp', 'RCL': 'Royal Caribbean', 'NCLH': 'Norwegian Cruise',
        'DKNG': 'DraftKings Inc', 'PENN': 'Penn Entertainment', 'MGM': 'MGM Resorts',
        'WYNN': 'Wynn Resorts',
        'TLRY': 'Tilray Brands', 'SNDL': 'SNDL Inc', 'CGC': 'Canopy Growth',
        'ACB': 'Aurora Cannabis',
        'BABA': 'Alibaba Group', 'JD': 'JD.com Inc', 'PDD': 'Pinduoduo Inc',
        'BIDU': 'Baidu Inc', 'NIO': 'NIO Inc',
        'UPST': 'Upstart Holdings', 'SOFI': 'SoFi Technologies', 'HOOD': 'Robinhood Markets',
        'RBLX': 'Roblox Corp', 'U': 'Unity Software', 'PATH': 'UiPath Inc',
        'KO': 'Coca-Cola Co', 'PEP': 'PepsiCo Inc', 'PG': 'Procter & Gamble',
        'MMM': '3M Company',
        'NEE': 'NextEra Energy', 'DUK': 'Duke Energy', 'SO': 'Southern Company',
        'D': 'Dominion Energy',
        'LIN': 'Linde PLC', 'APD': 'Air Products & Chem', 'ECL': 'Ecolab Inc',
        'SHW': 'Sherwin-Williams',
        'LMT': 'Lockheed Martin', 'RTX': 'RTX Corp', 'NOC': 'Northrop Grumman',
        'GD': 'General Dynamics'
    }
    return names.get(ticker, ticker)

def get_sector(ticker):
    sectors = {
        'AAPL': 'Technologie', 'MSFT': 'Technologie', 'NVDA': 'Technologie',
        'GOOGL': 'Technologie', 'AMZN': 'Consument', 'META': 'Technologie',
        'AMD': 'Technologie', 'INTC': 'Technologie', 'TSM': 'Technologie',
        'AVGO': 'Technologie', 'QCOM': 'Technologie', 'TXN': 'Technologie',
        'TSLA': 'Automotive', 'RIVN': 'Automotive', 'LCID': 'Automotive',
        'F': 'Automotive', 'GM': 'Automotive',
        'ORCL': 'Technologie', 'CRM': 'Technologie', 'ADBE': 'Technologie',
        'NOW': 'Technologie', 'INTU': 'Technologie', 'PLTR': 'Technologie',
        'NFLX': 'Communicatie', 'DIS': 'Communicatie', 'CMCSA': 'Communicatie',
        'PARA': 'Communicatie', 'WBD': 'Communicatie',
        'JPM': 'Financieel', 'BAC': 'Financieel', 'GS': 'Financieel',
        'MS': 'Financieel', 'WFC': 'Financieel', 'C': 'Financieel',
        'COIN': 'Financieel', 'MARA': 'Financieel', 'RIOT': 'Financieel',
        'CLSK': 'Financieel', 'HUT': 'Financieel',
        'V': 'Financieel', 'MA': 'Financieel', 'PYPL': 'Financieel',
        'SQ': 'Financieel', 'AFRM': 'Financieel',
        'WMT': 'Retail', 'TGT': 'Retail', 'COST': 'Retail',
        'HD': 'Retail', 'NKE': 'Consument', 'SBUX': 'Consument',
        'JNJ': 'Healthcare', 'UNH': 'Healthcare', 'PFE': 'Healthcare',
        'MRNA': 'Healthcare', 'REGN': 'Healthcare', 'GILD': 'Healthcare',
        'XOM': 'Energie', 'CVX': 'Energie', 'COP': 'Energie',
        'SLB': 'Energie', 'OXY': 'Energie',
        'CAT': 'Industrieel', 'BA': 'Industrieel', 'GE': 'Industrieel',
        'HON': 'Industrieel', 'UPS': 'Industrieel',
        'ASML.AS': 'Technologie', 'SAP': 'Technologie', 'NESN.SW': 'Consument',
        'NOVN.SW': 'Healthcare', 'AZN': 'Healthcare',
        'SNOW': 'Technologie', 'NET': 'Technologie', 'DDOG': 'Technologie',
        'ZS': 'Technologie', 'CRWD': 'Technologie', 'MDB': 'Technologie',
        'BIIB': 'Healthcare', 'VRTX': 'Healthcare', 'ALNY': 'Healthcare',
        'BMRN': 'Healthcare', 'INCY': 'Healthcare', 'TECH': 'Healthcare',
        'AMT': 'Vastgoed', 'PLD': 'Vastgoed', 'CCI': 'Vastgoed',
        'EQIX': 'Vastgoed', 'SPG': 'Vastgoed',
        'T': 'Communicatie', 'VZ': 'Communicatie', 'TMUS': 'Communicatie',
        'CHTR': 'Communicatie',
        'MCD': 'Consument', 'LULU': 'Consument', 'DECK': 'Consument',
        'CROX': 'Consument', 'SKX': 'Consument',
        'DAL': 'Transport', 'UAL': 'Transport', 'AAL': 'Transport',
        'LUV': 'Transport',
        'CCL': 'Consument', 'RCL': 'Consument', 'NCLH': 'Consument',
        'DKNG': 'Consument', 'PENN': 'Consument', 'MGM': 'Consument',
        'WYNN': 'Consument',
        'TLRY': 'Healthcare', 'SNDL': 'Healthcare', 'CGC': 'Healthcare',
        'ACB': 'Healthcare',
        'BABA': 'Consument', 'JD': 'Consument', 'PDD': 'Consument',
        'BIDU': 'Technologie', 'NIO': 'Automotive',
        'UPST': 'Financieel', 'SOFI': 'Financieel', 'HOOD': 'Financieel',
        'RBLX': 'Technologie', 'U': 'Technologie', 'PATH': 'Technologie',
        'KO': 'Consument', 'PEP': 'Consument', 'PG': 'Consument',
        'MMM': 'Industrieel',
        'NEE': 'Utilities', 'DUK': 'Utilities', 'SO': 'Utilities',
        'D': 'Utilities',
        'LIN': 'Materialen', 'APD': 'Materialen', 'ECL': 'Materialen',
        'SHW': 'Materialen',
        'LMT': 'Defensie', 'RTX': 'Defensie', 'NOC': 'Defensie',
        'GD': 'Defensie'
    }
    return sectors.get(ticker, 'Overig')

# ============= SITE GENERATION =============

def generate_main_site(results, today):
    """Generate the main index.html - complete financial platform"""
    
    date_str = today.strftime("%Y-%m-%d")
    date_display = today.strftime("%d %B %Y")
    
    # Market overview stats
    bullish = len([r for r in results if r['setup_score'] > 0])
    bearish = len([r for r in results if r['setup_score'] < 0])
    neutral = len(results) - bullish - bearish
    avg_upside = sum(r['potential_upside'] for r in results) / len(results) if results else 0
    
    # Top picks
    top_picks = [r for r in results if r['setup_score'] >= 2][:5]
    
    # Generate stock rows for market overview
    market_rows = ""
    for r in results[:10]:
        change_class = "positive" if r['change_pct'] >= 0 else "negative"
        change_sign = "+" if r['change_pct'] >= 0 else ""
        signal_class = r['signal_class']
        market_rows += f"""
        <tr class="stock-row" data-ticker="{r['ticker']}" data-sector="{r['sector']}" data-signal="{r['signal_class']}">
            <td class="ticker"><strong>{r['ticker']}</strong><br><small>{r['name']}</small></td>
            <td class="sector">{r['sector']}</td>
            <td class="price">€{r['price']:.2f}</td>
            <td class="change {change_class}">{change_sign}{r['change_pct']:.2f}%</td>
            <td class="volume">{r['volume']:,}</td>
            <td class="rsi">{r['rsi']:.1f}</td>
            <td class="signal {signal_class}">{r['signal']}</td>
            <td class="upside">+{r['potential_upside']:.1f}%</td>
        </tr>"""
    
    # Generate analysis cards
    analysis_cards = ""
    for i, pick in enumerate(top_picks[:3]):
        card_class = "featured" if i == 0 else ""
        analysis_cards += f"""
        <article class="analysis-card {card_class}">
            <header>
                <span class="ticker-badge">{pick['ticker']}</span>
                <span class="signal-badge {pick['signal_class']}">{pick['signal']}</span>
            </header>
            <h3>{pick['name']}</h3>
            <div class="price-block">
                <span class="price">€{pick['price']:.2f}</span>
                <span class="upside">Potentieel: +{pick['potential_upside']:.1f}%</span>
            </div>
            <div class="metrics">
                <div class="metric">
                    <span class="label">RSI</span>
                    <span class="value">{pick['rsi']:.1f}</span>
                </div>
                <div class="metric">
                    <span class="label">Setup</span>
                    <span class="value">{pick['setup_type']}</span>
                </div>
                <div class="metric">
                    <span class="label">Score</span>
                    <span class="value">{pick['setup_score']:.1f}/10</span>
                </div>
            </div>
            <ul class="reasons">
                {"".join([f"<li>✓ {r}</li>" for r in pick['setup_reasons'][:3]])}
            </ul>
            <a href="article/{date_str}.html#{pick['ticker']}" class="read-more">Lees analyse →</a>
        </article>"""
    
    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Dagelijkse beursanalyse en trading signals - AI-powered stock analysis">
    <meta name="theme-color" content="#059669">
    <title>Beurs Cowboy | Markt Analyse | {date_display}</title>
    <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
    <!-- Header -->
    <header class="site-header">
        <div class="header-container">
            <div class="logo">
                <a href="index.html" class="logo-link">
                    <span class="logo-icon">🤠</span>
                    <span class="logo-text">Beurs<span class="highlight">Cowboy</span></span>
                </a>
            </div>
            <button class="mobile-menu-toggle" id="mobileMenuToggle" aria-label="Menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <nav class="main-nav" id="mainNav">
                <a href="index.html" class="active">Markten</a>
                <a href="analysis.html">Analyse</a>
                <a href="watchlist.html">Watchlist</a>
                <a href="archive.html">Archief</a>
            </nav>
            <div class="header-actions">
                <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode">
                    <span class="icon-sun">☀️</span>
                    <span class="icon-moon">🌙</span>
                </button>
                <button class="search-toggle" id="searchToggle" aria-label="Search">
                    🔍
                </button>
            </div>
        </div>
    </header>

    <!-- Search Bar -->
    <div class="search-bar" id="searchBar">
        <div class="search-container">
            <input type="text" id="searchInput" placeholder="Zoek aandelen, sectoren, signals..." aria-label="Search">
            <button class="search-close" id="searchClose">✕</button>
        </div>
    </div>

    <!-- Market Ticker -->
    <div class="market-ticker">
        <div class="ticker-content">
            <span class="ticker-item">MARKT: {bullish} Bullisch | {bearish} Bearish | {neutral} Neutraal</span>
            <span class="ticker-item">GEM. POTENTIEEL: +{avg_upside:.1f}%</span>
            <span class="ticker-item">DATUM: {date_display}</span>
        </div>
    </div>

    <!-- Main Content -->
    <main class="main-content">
        <!-- Market Overview Section -->
        <section class="content-section">
            <div class="section-header">
                <h1>Markt Overzicht</h1>
                <p class="section-subtitle">Dagelijkse analyse en trading signals - {date_display}</p>
            </div>

            <!-- Market Stats Cards -->
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-icon">📊</span>
                    <div class="stat-content">
                        <span class="stat-value">{len(results)}</span>
                        <span class="stat-label">Aandelen Geanalyseerd</span>
                    </div>
                </div>
                <div class="stat-card bullish">
                    <span class="stat-icon">🟢</span>
                    <div class="stat-content">
                        <span class="stat-value">{bullish}</span>
                        <span class="stat-label">Bullische Signals</span>
                    </div>
                </div>
                <div class="stat-card bearish">
                    <span class="stat-icon">🔴</span>
                    <div class="stat-content">
                        <span class="stat-value">{bearish}</span>
                        <span class="stat-label">Bearish Signals</span>
                    </div>
                </div>
                <div class="stat-card">
                    <span class="stat-icon">🎯</span>
                    <div class="stat-content">
                        <span class="stat-value">+{avg_upside:.1f}%</span>
                        <span class="stat-label">Gem. Potentieel</span>
                    </div>
                </div>
            </div>

            <!-- Top Picks -->
            <div class="top-picks-section">
                <h2 class="section-title">Top Analyses</h2>
                <div class="analysis-grid">
                    {analysis_cards}
                </div>
            </div>

            <!-- Full Market Table -->
            <div class="market-table-section">
                <h2 class="section-title">Complete Markt</h2>
                <div class="table-filters">
                    <button class="filter-btn active" data-filter="all">Alle</button>
                    <button class="filter-btn" data-filter="buy">Koop</button>
                    <button class="filter-btn" data-filter="neutral">Neutraal</button>
                    <button class="filter-btn" data-filter="sell">Verkoop</button>
                </div>
                <div class="table-container">
                    <table class="market-table">
                        <thead>
                            <tr>
                                <th>Aandeel</th>
                                <th>Sector</th>
                                <th>Prijs</th>
                                <th>Verandering</th>
                                <th>Volume</th>
                                <th>RSI</th>
                                <th>Signal</th>
                                <th>Potentieel</th>
                            </tr>
                        </thead>
                        <tbody>
                            {market_rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="footer-container">
            <div class="footer-content">
                <div class="footer-section">
                    <h4>🤠 Beurs Cowboy</h4>
                    <p>Dagelijkse beursanalyse met een westelijk tintje. AI-powered, cowboy-goedgekeurd.</p>
                </div>
                <div class="footer-section">
                    <h4>Disclaimer</h4>
                    <p>Dit is geen financieel advies. Trading is als het wilde westen - er zijn schurken en er zijn sheriffs. Wees een sheriff.</p>
                </div>
                <div class="footer-section">
                    <h4>Data Bronnen</h4>
                    <p>Prijzen: Yahoo Finance<br>Sentiment: Qwen LLM<br>Wijsheid: Het Wilde Westen</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; {today.year} Beurs Cowboy. Yeehaw! 🤠 Alle rechten voorbehouden.</p>
            </div>
        </div>
    </footer>

    <script src="assets/main.js"></script>
    <script>
        // Search data
        const searchData = {{results: {json.dumps({"marketData": results})}}};
    </script>
</body>
</html>"""
    
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
        f.write(html)

def generate_article(results, today):
    """Generate detailed analysis article"""
    
    date_str = today.strftime("%Y-%m-%d")
    date_display = today.strftime("%d %B %Y")
    
    top_picks = [r for r in results if r['setup_score'] >= 2][:5]
    
    article_content = ""
    for i, pick in enumerate(top_picks):
        article_content += f"""
        <article class="stock-analysis" id="{pick['ticker']}">
            <header class="article-header">
                <div class="ticker-header">
                    <div>
                        <span class="ticker-badge large">{pick['ticker']}</span>
                        <span class="signal-badge {pick['signal_class']}">{pick['signal']}</span>
                    </div>
                    <div class="price-large">
                        <span class="price">€{pick['price']:.2f}</span>
                        <span class="change {'positive' if pick['change_pct'] >= 0 else 'negative'}">
                            {pick['change_pct']:+.2f}%
                        </span>
                    </div>
                </div>
                <h2>{pick['name']}</h2>
                <p class="sector">{pick['sector']}</p>
            </header>
            
            <div class="analysis-grid-2">
                <div class="analysis-card-detail">
                    <h3>Technische Analyse</h3>
                    <div class="detail-grid">
                        <div class="detail-item">
                            <span class="label">RSI</span>
                            <span class="value">{pick['rsi']:.1f}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">MACD</span>
                            <span class="value">{pick['macd']:.4f}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">SMA 20</span>
                            <span class="value">€{pick['sma_20']:.2f}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">SMA 50</span>
                            <span class="value">€{pick['sma_50']:.2f}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">52W High</span>
                            <span class="value">€{pick['high_52w']:.2f}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">52W Low</span>
                            <span class="value">€{pick['low_52w']:.2f}</span>
                        </div>
                    </div>
                </div>
                
                <div class="analysis-card-detail">
                    <h3>Trading Setup</h3>
                    <div class="setup-info">
                        <div class="setup-row">
                            <span class="label">Type:</span>
                            <span class="value">{pick['setup_type']}</span>
                        </div>
                        <div class="setup-row">
                            <span class="label">Score:</span>
                            <span class="value">{pick['setup_score']:.1f}/10</span>
                        </div>
                        <div class="setup-row">
                            <span class="label">Potentieel:</span>
                            <span class="value positive">+{pick['potential_upside']:.1f}%</span>
                        </div>
                        <div class="setup-row">
                            <span class="label">Volatiliteit:</span>
                            <span class="value">{pick['atr_pct']:.1f}% (Rank: {pick['vol_rank']:.0f})</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="analysis-content">
                <h3>Analyse</h3>
                <p>{pick['sentiment_summary']}</p>
                
                <h4>Key Levels</h4>
                <ul class="levels-list">
                    <li>Support: €{pick['sma_20']:.2f} (20-daags gemiddelde)</li>
                    <li>Resistance: €{pick['high_52w']:.2f} (52-week high)</li>
                </ul>
                
                <h4>Trading Advies</h4>
                <p class="advice">{generate_trading_advice(pick)}</p>
            </div>
        </article>"""
    
    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markt Analyse | {date_display} | MarketInsights</title>
    <link rel="stylesheet" href="../assets/styles.css">
</head>
<body>
    <header class="site-header">
        <div class="header-container">
            <div class="logo">
                <a href="../index.html" class="logo-link">
                    <span class="logo-icon">📈</span>
                    <span class="logo-text">Market<span class="highlight">Insights</span></span>
                </a>
            </div>
            <nav class="main-nav">
                <a href="../index.html">Markten</a>
                <a href="../analysis.html" class="active">Analyse</a>
                <a href="../watchlist.html">Watchlist</a>
                <a href="../archive.html">Archief</a>
            </nav>
            <div class="header-actions">
                <button class="theme-toggle" id="themeToggle">
                    <span class="icon-sun">☀️</span>
                    <span class="icon-moon">🌙</span>
                </button>
            </div>
        </div>
    </header>

    <main class="main-content article-page">
        <section class="content-section">
            <div class="section-header">
                <h1>Dagelijkse Markt Analyse</h1>
                <p class="section-subtitle">{date_display}</p>
            </div>
            
            <div class="analysis-articles">
                {article_content}
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="footer-container">
            <p>&copy; {today.year} MarketInsights. Geen financieel advies.</p>
        </div>
    </footer>

    <script src="../assets/main.js"></script>
</body>
</html>"""
    
    os.makedirs(os.path.join(OUTPUT_DIR, "article"), exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "article", f"{date_str}.html"), "w") as f:
        f.write(html)

def generate_trading_advice(pick):
    if pick['setup_type'] == "Trend Volgt":
        return f"{pick['ticker']} vertoont een sterke uptrend met prijs boven zowel het 20-daags als 50-daags gemiddelde. Het momentum is positief. Bij een dip naar €{pick['sma_20']:.2f} kan een instapkans ontstaan. Stop loss onder €{pick['sma_50']:.2f}."
    elif pick['setup_type'] == "Oversold Reversal":
        return f"{pick['ticker']} is oversold (RSI: {pick['rsi']:.1f}) en toont tekenen van herstel. Een bounce naar het 20-daags gemiddelde bij €{pick['sma_20']:.2f} is het eerste doel. Stop loss onder recent low."
    elif pick['setup_type'] == "MA Test":
        return f"{pick['ticker']} test het 20-daags gemiddelde. Dit is vaak een goed instappunt in een uptrend. Bij steun kan een move van {pick['potential_upside']:.1f%} mogelijk zijn."
    else:
        return f"Afwachten tot duidelijkere signals. {pick['ticker']} toont gemengde signalen. Wacht op bevestiging boven €{pick['sma_20']:.2f} voor long posities."

def save_snapshot(snapshot_data, date_str):
    snapshot_path = os.path.join(DATA_DIR, f"snap_{date_str}.json")
    with open(snapshot_path, "w") as f:
        json.dump(snapshot_data, f, indent=2)

def generate_search_data(results, date_str):
    """Generate search index JSON"""
    search_index = {
        "date": date_str,
        "stocks": [
            {
                "ticker": r['ticker'],
                "name": r['name'],
                "sector": r['sector'],
                "signal": r['signal'],
                "signal_class": r['signal_class']
            }
            for r in results
        ]
    }
    with open(os.path.join(OUTPUT_DIR, "search-index.json"), "w") as f:
        json.dump(search_index, f, indent=2)

if __name__ == "__main__":
    analyze()
