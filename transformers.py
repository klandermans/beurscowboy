"""
Data Transformers

Verantwoordelijk voor het transformeren van ruwe data:
- Technische indicatoren berekenen
- Setup scores berekenen
- Signalen genereren
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, List, Optional


def calculate_technical_indicators(
    hist: pd.DataFrame,
    params: Dict[str, int]
) -> Dict[str, float]:
    """
    Calculate all technical indicators for a ticker.
    
    Args:
        hist: Price history DataFrame
        params: Technical analysis parameters
    
    Returns:
        Dict with all calculated indicators
    """
    prices = hist['Close']
    
    # RSI
    rsi = _calculate_rsi(prices, params['rsi_window']).iloc[-1]
    
    # MACD
    macd_val, macd_signal, macd_hist = _calculate_macd(
        prices,
        params['macd_fast'],
        params['macd_slow'],
        params['macd_signal']
    )
    
    # SMAs
    sma_20 = prices.rolling(params['sma_short']).mean().iloc[-1]
    sma_50 = prices.rolling(params['sma_medium']).mean().iloc[-1] if len(prices) >= params['sma_medium'] else None
    
    # ATR
    atr = _calculate_atr(hist, params['atr_period'])
    atr_pct = (atr / prices.iloc[-1]) * 100
    
    # Volatility rank
    vol_rank = _get_volatility_rank(hist, params['volatility_period'])
    
    # 52-week high/low
    high_52w = hist['High'].max()
    low_52w = hist['Low'].min()
    
    # Volume
    volume = hist['Volume'].iloc[-1]
    
    return {
        'rsi': rsi,
        'macd': macd_val,
        'macd_signal': macd_signal,
        'macd_hist': macd_hist,
        'sma_20': sma_20,
        'sma_50': sma_50,
        'atr': atr,
        'atr_pct': atr_pct,
        'vol_rank': vol_rank,
        'high_52w': high_52w,
        'low_52w': low_52w,
        'volume': volume,
    }


def calculate_setup_score(
    indicators: Dict[str, float],
    current_price: float,
    avg_price: float,
    weights: Dict[str, float]
) -> Tuple[float, List[str]]:
    """
    Calculate setup score based on technical indicators.
    
    Args:
        indicators: Technical indicators dict
        current_price: Current price
        avg_price: Average price
        weights: Scoring weights
    
    Returns:
        Tuple of (score, reasons)
    """
    score = 0.0
    reasons = []
    
    rsi = indicators['rsi']
    macd_hist = indicators['macd_hist']
    macd_val = indicators['macd']
    macd_signal = indicators['macd_signal']
    sma_20 = indicators['sma_20']
    sma_50 = indicators['sma_50']
    atr_pct = indicators['atr_pct']
    
    # RSI scoring
    if 30 <= rsi <= 40:
        score += weights['rsi_oversold']
        reasons.append("RSI oversold - bounce kans")
    elif 60 <= rsi <= 70:
        score += weights['rsi_bullish']
        reasons.append("RSI in bullische zone")
    elif rsi < 30:
        score += weights['rsi_oversold'] * 0.5
        reasons.append("Diep oversold - reversal kans")
    elif rsi > 75:
        score -= weights['rsi_oversold']
        reasons.append("Overbought - correctie risico")
    
    # MACD scoring
    if macd_hist > 0 and macd_val > macd_signal:
        score += weights['macd_bullish']
        reasons.append("MACD bullisch momentum")
    elif macd_hist < 0 and macd_val < macd_signal:
        score -= weights['macd_bullish']
        reasons.append("MACD bearish momentum")
    
    # MA alignment
    if sma_20 and sma_50:
        if current_price > sma_20 > sma_50:
            score += weights['ma_alignment']
            reasons.append("Bullische MA alignement")
        elif current_price < sma_20 < sma_50:
            score -= weights['ma_alignment']
            reasons.append("Bearish MA alignement")
        elif abs(current_price - sma_20) / avg_price < 0.02:
            score += weights['ma_alignment'] * 0.5
            reasons.append("Test 20-daags gemiddelde")
    
    # Volatility
    if atr_pct > 3:
        score += weights['high_volatility']
        reasons.append(f"Hoge volatiliteit (ATR {atr_pct:.1f}%)")
    
    return score, reasons


def calculate_potential_upside(
    indicators: Dict[str, float],
    current_price: float
) -> float:
    """Calculate potential upside percentage"""
    sma_20 = indicators['sma_20']
    sma_50 = indicators['sma_50']
    high_52w = indicators['high_52w']
    atr = indicators['atr']
    
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


def get_trade_setup_type(
    indicators: Dict[str, float],
    current_price: float
) -> str:
    """Determine trade setup type"""
    rsi = indicators['rsi']
    macd_hist = indicators['macd_hist']
    sma_20 = indicators['sma_20']
    sma_50 = indicators['sma_50']
    
    if rsi < 30 and macd_hist > 0:
        return "Oversold Reversal"
    elif rsi > 70 and macd_hist < 0:
        return "Overbought Correctie"
    elif sma_20 and sma_50 and current_price > sma_20 > sma_50 and macd_hist > 0:
        return "Trend Volgt"
    elif sma_20 and sma_50 and current_price < sma_20 < sma_50 and macd_hist < 0:
        return "Downtrend Volgt"
    elif sma_20 and abs(current_price - sma_20) / sma_20 < 0.01:
        return "MA Test"
    elif 45 < rsi < 55:
        return "Consolidatie"
    else:
        return "Gemengd Signaal"


def get_signal(score: float, upside: float) -> Tuple[str, str]:
    """
    Determine trading signal based on score and upside.
    
    Returns:
        Tuple of (signal_text, signal_class)
    """
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


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _calculate_rsi(prices: pd.Series, window: int = 14) -> pd.Series:
    """Calculate RSI"""
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=window).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def _calculate_macd(
    prices: pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9
) -> Tuple[float, float, float]:
    """Calculate MACD"""
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    
    return macd_line.iloc[-1], signal_line.iloc[-1], histogram.iloc[-1]


def _calculate_atr(hist: pd.DataFrame, period: int = 14) -> float:
    """Calculate Average True Range"""
    high = hist['High']
    low = hist['Low']
    close = hist['Close'].shift(1)
    
    tr1 = high - low
    tr2 = abs(high - close)
    tr3 = abs(low - close)
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    return tr.rolling(period).mean().iloc[-1]


def _get_volatility_rank(hist: pd.DataFrame, period: int = 252) -> float:
    """Calculate volatility rank"""
    if len(hist) < period:
        return 50
    
    daily_returns = hist['Close'].pct_change()
    current_vol = daily_returns.rolling(20).std().iloc[-1]
    vol_rank = (daily_returns.rolling(20).std() < current_vol).sum() / (period - 20) * 100
    
    return vol_rank
