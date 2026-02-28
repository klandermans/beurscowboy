"""
Sentiment Analyzers

Verantwoordelijk voor sentiment analyse:
- Batch LLM sentiment
- Regionale macro sentiment
- Keyword-based fallback
"""

import re
import json
from typing import Dict, List, Any, Optional

try:
    from qwen_agent.agents import Assistant
    QWEN_AVAILABLE = True
except ImportError:
    QWEN_AVAILABLE = False


def analyze_sentiment_batch(
    ticker_headlines: Dict[str, List[str]],
    keywords: Dict[str, List[str]]
) -> Dict[str, Dict[str, Any]]:
    """
    Analyze sentiment for multiple tickers using LLM with keyword fallback.
    
    Args:
        ticker_headlines: Dict of {ticker: [headlines]}
        keywords: Sentiment keywords for fallback
    
    Returns:
        Dict of sentiment results per ticker
    """
    if not ticker_headlines:
        return {}
    
    # Try LLM first
    if QWEN_AVAILABLE:
        try:
            llm_result = _get_llm_batch_sentiment(ticker_headlines)
            if llm_result:
                return llm_result
        except Exception as e:
            print(f"  ⚠️ LLM failed, using keyword fallback: {e}")
    
    # Fallback to keyword-based
    return _get_keyword_batch_sentiment(ticker_headlines, keywords)


def analyze_regional_sentiment(
    regional_news: Dict[str, List[Dict]],
    macro_keywords: Dict[str, List[str]]
) -> Dict[str, Dict[str, Any]]:
    """
    Analyze macro-economic sentiment per region.
    
    Args:
        regional_news: Dict of {region: [articles]}
        macro_keywords: Macro sentiment keywords
    
    Returns:
        Dict of regional sentiment results
    """
    regional_sentiment = {}
    
    for region, articles in regional_news.items():
        if not articles:
            regional_sentiment[region] = {
                'score': 0.0,
                'articles_count': 0,
                'sentiment': 'Neutraal'
            }
            continue
        
        positive_count = 0
        negative_count = 0
        
        for article in articles:
            text = (article['title'] + ' ' + article.get('summary', '')).lower()
            positive_count += sum(1 for kw in macro_keywords['positive'] if kw in text)
            negative_count += sum(1 for kw in macro_keywords['negative'] if kw in text)
        
        total = positive_count + negative_count
        score = (positive_count - negative_count) / total if total > 0 else 0.0
        
        # Determine sentiment label
        if score > 0.2:
            sentiment = 'Positief'
        elif score < -0.2:
            sentiment = 'Negatief'
        else:
            sentiment = 'Neutraal'
        
        regional_sentiment[region] = {
            'score': round(score, 2),
            'articles_count': len(articles),
            'sentiment': sentiment,
            'positive': positive_count,
            'negative': negative_count
        }
    
    return regional_sentiment


def get_keyword_sentiment(
    ticker: str,
    headlines: List[str],
    keywords: Dict[str, List[str]]
) -> Dict[str, Any]:
    """
    Keyword-based sentiment analysis for single ticker.
    
    Args:
        ticker: Ticker symbol
        headlines: List of headlines
        keywords: Sentiment keywords
    
    Returns:
        Sentiment dict with score, summary, catalyst
    """
    if not headlines:
        return {"score": 0.0, "summary": "Geen nieuws", "catalyst": "Geen"}
    
    valid_headlines = [h for h in headlines[:5] if h]
    if not valid_headlines:
        return {"score": 0.0, "summary": "Geen nieuws", "catalyst": "Geen"}
    
    scores = []
    for headline in valid_headlines:
        text_lower = headline.lower()
        positive_count = sum(1 for k in keywords['positive'] if k in text_lower)
        negative_count = sum(1 for k in keywords['negative'] if k in text_lower)
        total = positive_count + negative_count
        score = (positive_count - negative_count) / total if total > 0 else 0.0
        scores.append(score)
    
    avg_score = sum(scores) / len(scores) if scores else 0.0
    
    # Summary
    if avg_score > 0.3:
        summary = "Overwegend positief nieuws"
    elif avg_score < -0.3:
        summary = "Overwegend negatief nieuws"
    else:
        summary = "Gemengd nieuws, geen duidelijke trend"
    
    # Catalyst detection
    all_text = " ".join(valid_headlines).lower()
    catalyst = "Geen specifieke catalyst"
    
    catalyst_keywords = {
        'Komende kwartaalcijfers': ['earnings', 'kwartaal', 'resultaat'],
        'Nieuwe productaankondiging': ['product', 'lanceert', 'nieuwe'],
        'Zakelijke ontwikkeling': ['deal', 'contract', 'partnership'],
        'Analisten advies wijziging': ['upgrade', 'downgrade', 'advies'],
    }
    
    for cat, kw_list in catalyst_keywords.items():
        if any(k in all_text for k in kw_list):
            catalyst = cat
            break
    
    return {
        "score": round(avg_score, 2),
        "summary": summary,
        "catalyst": catalyst
    }


# =============================================================================
# PRIVATE HELPER FUNCTIONS
# =============================================================================

def _get_llm_batch_sentiment(ticker_headlines: Dict[str, List[str]]) -> Optional[Dict]:
    """Get batch sentiment from LLM"""
    if not ticker_headlines or not QWEN_AVAILABLE:
        return None
    
    # Prepare input
    input_text = ""
    tickers = list(ticker_headlines.keys())
    
    for ticker in tickers:
        headlines = ticker_headlines[ticker][:7]  # Max 7 headlines
        if headlines:
            headlines_text = "\n".join(f"  - {h}" for h in headlines if h)
            input_text += f"\n{ticker}:\n{headlines_text}\n"
    
    if not input_text.strip():
        return None
    
    # Prompt
    prompt = f"""Je bent een financiële sentiment analist. Analyseer het nieuws voor deze aandelen:

{input_text}

Geef je antwoord ALS ALLEEN EEN JSON OBJECT in dit formaat:
{{
    "TICKER1": {{"score": <getal -1.0 tot 1.0>, "summary": "<1 zin>", "catalyst": "<catalyst of 'Geen'>"}},
    "TICKER2": {{"score": <getal -1.0 tot 1.0>, "summary": "<1 zin>", "catalyst": "<catalyst of 'Geen'>"}},
    ...
}}

Score richtlijnen:
- Zeer negatief (-1.0 tot -0.6): slechte cijfers, ontslagen, schandalen
- Negatief (-0.6 tot -0.3): tegenvallers, waarschuwingen
- Neutraal (-0.3 tot 0.3): gemengd, geen duidelijke trend
- Positief (0.3 tot 0.6): goede cijfers, groei, partnerships
- Zeer positief (0.6 tot 1.0): records, doorbraken, upgrades

Geef ALLEEN de JSON terug, geen uitleg."""
    
    try:
        llm_config = {'model': 'qwen-plus'}
        bot = Assistant(llm=llm_config)
        
        messages = [{'role': 'user', 'content': prompt}]
        response = bot.run(messages=messages)
        
        response_text = response if isinstance(response, str) else str(response)
        
        # Extract JSON
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            result = json.loads(json_match.group())
            
            sentiments = {}
            for ticker in tickers:
                if ticker in result:
                    sentiments[ticker] = {
                        "score": round(float(result[ticker].get("score", 0.0)), 2),
                        "summary": result[ticker].get("summary", "Gemengd nieuws"),
                        "catalyst": result[ticker].get("catalyst", "Geen")
                    }
                else:
                    sentiments[ticker] = {"score": 0.0, "summary": "Geen analyse", "catalyst": "Geen"}
            
            return sentiments
    
    except Exception as e:
        raise Exception(f"LLM error: {e}")
    
    return None


def _get_keyword_batch_sentiment(
    ticker_headlines: Dict[str, List[str]],
    keywords: Dict[str, List[str]]
) -> Dict[str, Dict[str, Any]]:
    """Get batch sentiment using keyword fallback"""
    sentiments = {}
    for ticker, headlines in ticker_headlines.items():
        sentiments[ticker] = get_keyword_sentiment(ticker, headlines, keywords)
    return sentiments
