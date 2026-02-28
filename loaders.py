"""
Output Loaders

Verantwoordelijk voor het genereren van output:
- HTML pagina's
- Data snapshots
- Search index
"""

import os
import json
import glob
import datetime
from typing import Dict, List, Any

from config import COMPANY_NAMES, SECTORS, SETTINGS


def generate_main_site(
    results: List[Dict],
    today: datetime.date,
    trending_stocks: List[Dict],
    regional_sentiment: Dict
) -> None:
    """Generate main index.html"""
    date_str = today.strftime("%Y-%m-%d")
    date_display = today.strftime("%d %B %Y")
    
    output_dir = SETTINGS['output_dir']
    os.makedirs(output_dir, exist_ok=True)
    
    # Stats
    bullish = len([r for r in results if r['setup_score'] > 0])
    bearish = len([r for r in results if r['setup_score'] < 0])
    neutral = len(results) - bullish - bearish
    
    # Top picks
    top_picks = [r for r in results if r['setup_score'] >= 2][:5]
    
    # Generate HTML sections
    market_rows = _generate_market_rows(results[:10])
    analysis_cards = _generate_analysis_cards(top_picks[:3], date_str)
    macro_section = _generate_macro_section(regional_sentiment)
    trending_section = _generate_trending_section(trending_stocks)
    
    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Beurs Cowboy | Markt Analyse | {date_display}</title>
    <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
    <!-- Header en navigatie -->
    <header class="site-header">
        <div class="header-container">
            <div class="logo">
                <a href="index.html" class="logo-link">
                    <span class="logo-icon">🤠</span>
                    <span class="logo-text">Beurs<span class="highlight">Cowboy</span></span>
                </a>
            </div>
            <nav class="main-nav">
                <a href="index.html" class="active">Markten</a>
                <a href="analysis.html">Analyse</a>
                <a href="watchlist.html">Watchlist</a>
                <a href="archive.html">Archief</a>
            </nav>
        </div>
    </header>

    <main class="main-content">
        <section class="content-section">
            <div class="section-header">
                <h1>Markt Analyse</h1>
                <p class="section-subtitle">{date_display}</p>
            </div>

            <!-- Macro Sentiment -->
            {macro_section}

            <!-- Trending -->
            {trending_section}

            <!-- Top Picks -->
            <div class="top-picks-section">
                <h2 class="section-title">Top Analyses</h2>
                <div class="analysis-grid">
                    {analysis_cards}
                </div>
            </div>

            <!-- Complete Market Table -->
            <div class="market-table-section">
                <h2 class="section-title">Complete Markt</h2>
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

    <footer class="site-footer">
        <div class="footer-container">
            <div class="footer-content">
                <div class="footer-section">
                    <h4>🤠 Beurs Cowboy</h4>
                    <p>Dagelijkse beursanalyse met een westelijk tintje.</p>
                </div>
                <div class="footer-section">
                    <h4>Disclaimer</h4>
                    <p>Dit is geen financieel advies.</p>
                </div>
            </div>
        </div>
    </footer>

    <script src="assets/main.js"></script>
</body>
</html>"""
    
    with open(os.path.join(output_dir, "index.html"), "w") as f:
        f.write(html)


def generate_article(results: List[Dict], today: datetime.date) -> None:
    """Generate detailed article"""
    # Implementation volgt...
    pass


def generate_watchlist(results: List[Dict], today: datetime.date) -> None:
    """Generate watchlist.html"""
    # Implementation volgt...
    pass


def generate_archive(
    results: List[Dict],
    today: datetime.date,
    data_dir: str
) -> None:
    """Generate archive.html"""
    # Implementation volgt...
    pass


def generate_ticker_pages(results: List[Dict], output_dir: str) -> None:
    """Generate individual ticker pages"""
    ticker_dir = os.path.join(output_dir, "ticker")
    os.makedirs(ticker_dir, exist_ok=True)
    
    for r in results:
        html = _generate_ticker_page_html(r)
        output_path = os.path.join(ticker_dir, f"{r['ticker']}.html")
        with open(output_path, "w") as f:
            f.write(html)
    
    print(f"  ✓ {len(results)} ticker pagina's gegenereerd")


def save_snapshot(
    snapshot_data: Dict,
    date_str: str,
    data_dir: str
) -> None:
    """Save data snapshot"""
    os.makedirs(data_dir, exist_ok=True)
    
    output_path = os.path.join(data_dir, f"snap_{date_str}.json")
    with open(output_path, "w") as f:
        json.dump(snapshot_data, f, indent=2)


def generate_search_data(
    results: List[Dict],
    date_str: str,
    output_dir: str
) -> None:
    """Generate search index"""
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
    
    with open(os.path.join(output_dir, "search-index.json"), "w") as f:
        json.dump(search_index, f, indent=2)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _generate_market_rows(results: List[Dict]) -> str:
    """Generate market table rows"""
    rows = ""
    for r in results:
        change_class = "positive" if r['change_pct'] >= 0 else "negative"
        change_sign = "+" if r['change_pct'] >= 0 else ""
        trending_badge = "🔥" if r.get('is_trending') else ""
        
        rows += f"""
        <tr class="stock-row">
            <td class="ticker">
                <a href="ticker/{r['ticker']}.html" class="ticker-link">
                    <strong>{r['ticker']}</strong>{trending_badge}
                </a>
                <br><small>{r['name']}</small>
            </td>
            <td class="sector">{r['sector']}</td>
            <td class="price">€{r['price']:.2f}</td>
            <td class="change {change_class}">{change_sign}{r['change_pct']:.2f}%</td>
            <td class="volume">{r['volume']:,}</td>
            <td class="rsi">{r['rsi']:.1f}</td>
            <td class="signal {r['signal_class']}">{r['signal']}</td>
            <td class="upside">+{r['potential_upside']:.1f}%</td>
        </tr>"""
    
    return rows


def _generate_analysis_cards(picks: List[Dict], date_str: str) -> str:
    """Generate analysis cards"""
    cards = ""
    for i, pick in enumerate(picks):
        card_class = "featured" if i == 0 else ""
        reasons = "".join([f"<li>✓ {r}</li>" for r in pick['setup_reasons'][:3]])
        
        cards += f"""
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
            <ul class="reasons">
                {reasons}
            </ul>
            <a href="article/{date_str}.html#{pick['ticker']}" class="read-more">Lees analyse →</a>
        </article>"""
    
    return cards


def _generate_macro_section(regional_sentiment: Dict) -> str:
    """Generate macro sentiment section"""
    if not regional_sentiment:
        return ""
    
    sorted_regions = sorted(
        regional_sentiment.items(),
        key=lambda x: x[1].get('score', 0),
        reverse=True
    )[:SETTINGS['max_regional_display']]
    
    rows = ""
    for region, data in sorted_regions:
        if data['articles_count'] == 0:
            continue
        
        emoji = "🟢" if data['sentiment'] == 'Positief' else "🔴" if data['sentiment'] == 'Negatief' else "⚪"
        score_color = "#22c55e" if data['score'] > 0.2 else "#ef4444" if data['score'] < -0.2 else "var(--text-muted)"
        
        rows += f"""
        <div class="region-item">
            <div class="region-header">
                <span class="region-name">{emoji} {region}</span>
                <span class="region-sentiment" style="color: {score_color}">
                    {data['sentiment']} ({data['score']:+.2f})
                </span>
            </div>
            <div class="region-stats">
                <span class="stat">{data['articles_count']} artikelen</span>
                <span class="stat">🟢 {data.get('positive', 0)}</span>
                <span class="stat">🔴 {data.get('negative', 0)}</span>
            </div>
        </div>"""
    
    return f"""
    <section class="macro-section">
        <h2>🌍 Macro-economisch Sentiment</h2>
        <p class="section-subtitle">Wereldwijd economisch sentiment per regio</p>
        <div class="macro-grid">
            {rows}
        </div>
    </section>"""


def _generate_trending_section(trending_stocks: List[Dict]) -> str:
    """Generate trending stocks section"""
    if not trending_stocks:
        return ""
    
    rows = ""
    for t in trending_stocks[:SETTINGS['max_trending_display']]:
        wl_count = t.get('stocktwits_watchlist', 0)
        
        rows += f"""
        <div class="trending-item">
            <span class="trending-ticker">{t['ticker']}</span>
            <span class="trending-social">💬 {wl_count:,} volgers</span>
            <span class="trending-price">€{t['price']:.2f}</span>
            <span class="trending-change {'positive' if t['change_pct'] >= 0 else 'negative'}">
                {'+' if t['change_pct'] >= 0 else ''}{t['change_pct']:.1f}%
            </span>
        </div>"""
    
    return f"""
    <section class="trending-section">
        <h2>💬 Trending op Social Media</h2>
        <p class="section-subtitle">Meest besproken aandelen vandaag</p>
        <div class="trending-grid">
            {rows}
        </div>
    </section>"""


def _generate_ticker_page_html(r: Dict) -> str:
    """Generate single ticker page HTML"""
    # Implementation voor ticker detail pagina
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>{r['ticker']} - {r['name']} | Beurs Cowboy</title>
</head>
<body>
    <h1>{r['ticker']}</h1>
    <p>{r['name']}</p>
    <p>Prijs: €{r['price']:.2f}</p>
    <p>Signal: {r['signal']}</p>
</body>
</html>"""
