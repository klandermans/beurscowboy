# 🤠 Beurs Cowboy - TODO & Feature Requests

## ✅ Voltooid

- [x] **qwen-agent dependency** - Toegevoegd aan requirements.txt voor GitHub Actions
- [x] **Archief functionaliteit** - Automatische generatie van archive.html met timestamps
- [x] **RSS feeds uitgebreid** - 12 nieuwsbronnen i.p.v. 3
  - MarketWatch, Reuters, Yahoo Finance
  - TechCrunch, Seeking Alpha
  - Bloomberg, CNBC, Financial Times
  - CoinDesk, Benzinga
- [x] **Meer headlines** - 10 headlines per ticker i.p.v. 3
- [x] **StockTwits trending** - Trending sectie op homepage met watchlist counts
- [x] **Sentiment analyse verbeterd** - 7 headlines per ticker voor LLM i.p.v. 3

---

## 📋 Pending Features

### Prioriteit 1 - Belangrijk

- [ ] **Ticker-specifiek nieuws beter matchen**
  - Gebruik ticker symbolen in RSS feed zoekopdrachten
  - Filter RSS artikelen op ticker mentions
  - Voorbeeld: "AAPL" of "Apple" in titel/summary
  
- [ ] **Sentiment analyse per sectie verbeteren**
  - Aparte scores voor: kop, summary, content
  - Weeg recente artikelen zwaarder
  - Herken sarcasme/ironie beter

- [ ] **GitHub Actions workflow optimaliseren**
  - Cache dependencies voor snellere runs
  - Retry logic voor API failures
  - Betere error reporting

### Prioriteit 2 - Nice to Have

- [ ] **Meer technische indicatoren**
  - Bollinger Bands
  - Fibonacci levels
  - Volume analyse

- [ ] **Portfolio tracking**
  - Huidige posities bijhouden
  - P/L berekening
  - Performance metrics

- [ ] **Prijs alerts**
  - Email notificaties bij prijsdoelen
  - Push notifications

### Prioriteit 3 - Experimenteel

- [ ] **Backtesting module**
  - Test trading strategies op historische data
  - Performance statistieken

- [ ] **Machine Learning voorspellingen**
  - Price prediction models
  - Trend detection

- [ ] **Social sentiment uitbreiden**
  - Reddit r/wallstreetbets scraping
  - Twitter/X sentiment (als API gratis wordt)

---

## 🐛 Bekende Issues

1. **Yahoo Finance headlines** - Werkt niet altijd buiten beursuren
   - *Workaround:* RSS feeds als fallback

2. **StockTwits API** - Vereist nu authenticatie voor messages
   - *Workaround:* Alleen watchlist count gebruiken

3. **LLM rate limiting** - Qwen API kan timeouten bij veel requests
   - *Workaround:* Batch processing, retry logic

---

## 📊 Statistieken

| Metric | Huidig | Doel |
|--------|--------|------|
| RSS bronnen | 12 | 20 |
| Headlines per ticker | 10 | 15 |
| Sentiment accuracy | ~70% | 85% |
| API calls per run | ~150 | ~100 |
| Run tijd | ~90s | <60s |

---

## 🚀 Snel Start

```bash
# Installeer dependencies
pip install -r requirements.txt

# Run analyse
python stock_analyzer.py

# Test lokaal
python -m http.server 8000 -d docs
```

---

## 📝 Notities

### RSS Feed URLs om toe te voegen
- Barron's: `https://www.barrons.com/xml/rss/`
- The Motley Fool: `https://www.fool.com/feeds/latest/`
- Zacks: `https://www.zacks.com/stock/news/rss`

### Verbeteringen Sentiment Analyse
- Voeg context-aware keywords toe
- Gebruik sector-specifieke sentiment
- Weeg breaking news zwaarder

### Performance Optimalisatie
- Parallelle API calls voor RSS feeds
- Cache resultaten tussen runs
- Incremental updates i.p.v. full rebuild

---

**Laatste update:** 25 februari 2026  
**Versie:** 1.2.0
