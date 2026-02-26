# 🤠 Beurs Cowboy - TODO & Feature Requests

## ✅ Voltooid

- [x] **qwen-agent dependency** - Toegevoegd aan requirements.txt voor GitHub Actions
- [x] **Archief functionaliteit** - Automatische generatie van archive.html met timestamps
- [x] **RSS feeds uitgebreid** - 41 nieuwsbronnen wereldwijd!
  - **Noord-Amerika:** MarketWatch, Bloomberg, CNBC, Seeking Alpha, Barron's, Motley Fool, Benzinga
  - **Europa:** Financial Times, Handelsblatt, Les Echos, Il Sole 24 Ore, Expansion
  - **China:** China Daily, SCMP, Xinhua, Caixin
  - **Japan:** Nikkei Asia, Japan Times, NHK World
  - **Zuid-Korea:** Korea Herald, Korea Times
  - **Zuid-Oost Azië:** Straits Times, Bangkok Post
  - **Australië & Oceanië:** AFR, ABC News AU, Sydney Morning Herald, NZ Herald
  - **Midden-Oosten:** Arabian Business, Gulf News
  - **Afrika:** Business Day Live, Fin24
  - **Latijns-Amerika:** Valor Econômico, El Economista
  - **Tech & Crypto:** TechCrunch, CoinDesk, Cointelegraph
- [x] **Meer headlines** - 10 headlines per ticker i.p.v. 3
- [x] **StockTwits trending** - Trending sectie op homepage met watchlist counts
- [x] **Sentiment analyse verbeterd** - 7 headlines per ticker voor LLM i.p.v. 3
- [x] **Datum filtering** - Filtert nieuws op laatste 2 dagen (vandaag + gisteren)
  - RSS feeds: datum parsing met multiple formaten
  - Yahoo Finance: providerPublishTime filtering
  - Timezone-aware vergelijking
- [x] **Ticker detailpagina's** - TradingView widget voor elk aandeel
  - 136 individuele ticker pagina's
  - Interactieve charts met RSI, MACD, Moving Averages
  - Key metrics grid
  - Analyse sectie met sentiment en redenen
- [x] **Social Media trending sectie** - Subtielere styling
  - "💬 Trending op Social Media" i.p.v. StockTwits branding
  - Past beter in het Beurs Cowboy thema
  - Hover effects en subtiele kleuren

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

1. **RSS feeds timeout** - Sommige internationale feeds zijn traag of onbereikbaar
   - *Huidig:* 14/41 feeds succesvol (~34%)
   - *Workaround:* Timeout handling, fallback naar andere bronnen

2. **Yahoo Finance headlines** - Werkt niet altijd buiten beursuren
   - *Workaround:* RSS feeds als fallback

3. **StockTwits API** - Vereist nu authenticatie voor messages
   - *Workaround:* Alleen watchlist count gebruiken

4. **LLM rate limiting** - Qwen API kan timeouten bij veel requests
   - *Workaround:* Batch processing, retry logic

---

## 📊 Statistieken

| Metric | Huidig | Doel |
|--------|--------|------|
| RSS bronnen | 41 | 50 |
| Succesvolle feeds | 14 | 35+ |
| Headlines per ticker | 10 | 15 |
| Datum filtering | 2 dagen | 1 dag |
| Wereldwijde dekking | 6 continenten | ✅ |
| Sentiment accuracy | ~70% | 85% |
| API calls per run | ~200 | ~150 |
| Run tijd | ~120s | <90s |

---

## 🌍 Nieuwsbronnen per Regio

| Regio | Aantal Bronnen | Succesrate |
|-------|---------------|------------|
| Noord-Amerika | 9 | ~80% |
| Europa | 7 | ~60% |
| China | 4 | ~25% |
| Japan | 3 | ~33% |
| Zuid-Korea | 2 | ~50% |
| Zuid-Oost Azië | 2 | ~50% |
| Australië & Oceanië | 4 | ~75% |
| Midden-Oosten | 2 | ~50% |
| Afrika | 2 | ~50% |
| Latijns-Amerika | 2 | ~50% |
| Tech & Crypto | 3 | ~67% |

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
- India: Economic Times, Mint
- Rusland: TASS, RIA Novosti (beperkt beschikbaar)
- Scandinavië: Dagens Industri, Helsingin Sanomat

### Verbeteringen Sentiment Analyse
- Voeg context-aware keywords toe
- Gebruik sector-specifieke sentiment
- Weeg breaking news zwaarder
- Vertaal niet-Engelse artikelen

### Performance Optimalisatie
- Parallelle API calls voor RSS feeds
- Cache resultaten tussen runs
- Incremental updates i.p.v. full rebuild
- Timeout verlagen voor trage feeds

---

**Laatste update:** 25 februari 2026  
**Versie:** 1.4.0 - Wereldwijde Editie 🌍
