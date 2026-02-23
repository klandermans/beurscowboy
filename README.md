# 🤠 Beurs Cowboy

**Dagelijkse beursanalyse - Volledig Gratis!**

> "Trading is als het wilde westen - er zijn schurken en er zijn sheriffs. Wees een sheriff."

---

## ✨ Volledig Gratis!

Geen credit card nodig, geen API keys:

- ✅ **Yahoo Finance** - Gratis data en nieuws
- ✅ **RSS Feeds** - Gratis markt nieuws
- ✅ **Keyword Sentiment** - Geen dure LLM API's
- ✅ **GitHub Actions** - Gratis automation
- ✅ **GitHub Pages** - Gratis hosting

---

## Over Beurs Cowboy

Beurs Cowboy is een **100% gratis** geautomatiseerd platform dat dagelijks marktanalyses genereert:

- 📊 **Technische Analyse** - RSI, MACD, Moving Averages, ATR
- 📰 **Nieuws Analyse** - Yahoo Finance + RSS feeds
- 🎯 **Trading Signals** - Koop/Verkoop aanbevelingen
- 📱 **Volledig Responsive** - Mobiel, tablet, desktop
- 🌓 **Dark Mode** - Oogvriendelijk
- 🔍 **Zoekfunctie** - Snel aandelen vinden

---

## 🔄 Hoe Het Werkt

### Dagelijkse Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  1. GitHub Actions trigger (06:30 UTC of handmatig)            │
│                    ↓                                            │
│  2. Python script start op GitHub runner                        │
│                    ↓                                            │
│  3. Haalt 138+ aandelen op via Yahoo Finance                    │
│     - Prijs, volume, RSI, MACD, Moving Averages                 │
│     - 52-week high/low, ATR (volatiliteit)                      │
│                    ↓                                            │
│  4. LLM Sentiment Analyse (Qwen)                                │
│     - Analyseert nieuws headlines per aandeel                   │
│     - Bepaalt sentiment score (-1.0 tot 1.0)                    │
│     - Identificeert catalysten                                  │
│     - Fallback naar keyword analyse bij fout                    │
│                    ↓                                            │
│  5. Berekent technische setups                                  │
│     - Trend analyse (bullish/bearish)                           │
│     - Momentum signals                                          │
│     - Potentiële upside                                         │
│                    ↓                                            │
│  6. Genereert HTML pagina's                                     │
│     - index.html (markt overzicht)                              │
│     - analysis.html (gedetailleerde analyse)                    │
│     - watchlist.html (aandelen om te volgen)                    │
│     - archive.html (historie)                                   │
│                    ↓                                            │
│  7. Commit & push naar docs/ folder                             │
│                    ↓                                            │
│  8. GitHub Pages publiceert site automatisch                    │
└─────────────────────────────────────────────────────────────────┘
```

### LLM Sentiment Analyse

Het script gebruikt **Qwen** (via Dashscope) voor sentiment analyse:

| Feature | Beschrijving |
|---------|--------------|
| **Model** | Qwen-plus (gratis tier) |
| **Input** | Tot 5 nieuws headlines per aandeel |
| **Output** | Score (-1.0 tot 1.0), summary, catalyst |
| **Fallback** | Keyword-based analyse bij API fout |

**API Key Setup (Optioneel):**
- Zonder API key: gebruikt keyword-based sentiment (werkt prima!)
- Met API key: gebruikt LLM voor slimmere analyse
- Gratis tier: 100 requests/dag (voldoet voor 138 aandelen)

**Dashscope API Key aanvragen:**
1. Ga naar: https://dashscope.console.aliyun.com/
2. Maak account aan (gratis)
3. Maak API key aan
4. Voeg toe aan GitHub Secrets als `DASHSCOPE_API_KEY`

### Technische Analyse

Het script berekent voor elk aandeel:

| Indicator | Beschrijving | Gebruik |
|-----------|--------------|---------|
| **RSI** | Relative Strength Index (14 dagen) | Bepaalt overbought/oversold |
| **MACD** | Moving Average Convergence Divergence | Momentum indicator |
| **SMA 20/50** | Simple Moving Average | Trend richting |
| **ATR** | Average True Range | Volatiliteit |
| **Volume Rank** | Volume t.o.v. afgelopen jaar | Handelsactiviteit |

### Signal Berekening

```python
# Vereenvoudigde logica
setup_score = RSI_score + MACD_score + MA_alignement + volatiliteit
sentiment_score = keyword_analyse(nieuws_headlines)
totaal_score = setup_score + (sentiment_score * 3)

if totaal_score >= 4 AND upside >= 5%:
    signal = "Sterk Koop"
elif totaal_score >= 2:
    signal = "Koop"
elif totaal_score >= 0:
    signal = "Neutraal"
elif totaal_score >= -2:
    signal = "Voorzichtig"
else:
    signal = "Verkoop"
```

### Watchlist Logica

De watchlist toont aandelen die:
- Een positieve setup score hebben (`>= 0`)
- Nog geen duidelijk "Koop" signaal hebben (`Neutraal` of `Voorzichtig`)
- Minimaal 2% potentieel hebben
- Maximaal 15 resultaten

Dit zijn aandelen die je in de gaten moet houden - ze kunnen interessant worden als ze bepaalde niveaus breken.

---

## ⚠️ Disclaimer

**Dit is GEEN financieel advies.**

- Trading in aandelen brengt risico's met zich mee
- Dit platform is voor educatieve doeleinden
- Raadpleeg een financial advisor voor persoonlijk advies
- Trade nooit met geld dat je niet kunt verliezen

---

## 🚀 Quick Start (5 minuten)

### 1. Repository Clonen

```bash
git clone https://github.com/jouw-username/stockker.git
cd stockker
```

### 2. Dependencies Installeren

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Lokaal Testen

```bash
python stock_analyzer.py
```

Open `docs/index.html` in je browser.

**That's it!** Geen API keys, geen gedoe.

---

## 🌐 GitHub Pages Setup (Optioneel)

### Stap 1: Enable GitHub Pages

1. Ga naar **Settings** → **Pages**
2. Kies **Deploy from a branch**
3. Branch: **main** → Folder: **/docs**
4. Klik **Save**

### Stap 2: Workflow Testen

1. Ga naar **Actions** → **🤠 Beurs Cowboy**
2. Klik **Run workflow**
3. Wacht ~2 minuten

### Stap 3: Site Bekijken

Je site is nu beschikbaar op:
```
https://jouw-username.github.io/jouw-repo/
```

**Geen secrets nodig!** Alles is gratis.

---

## 📁 Bestandsstructuur

```
stockker/
├── stock_analyzer.py          # Main script (gratis analyse)
├── requirements.txt           # Python dependencies (allemaal gratis)
├── README.md                  # Deze handleiding
├── .github/workflows/
│   └── main.yml              # GitHub Actions (gratis CI/CD)
├── docs/                      # Website (gratis hosting op GitHub Pages)
│   ├── index.html            # Homepage
│   ├── analysis.html         # Analyse pagina
│   ├── watchlist.html        # Watchlist
│   ├── archive.html          # Archief
│   └── assets/
│       ├── styles.css        # Styling
│       └── main.js           # Interactive
└── data_snapshots/           # Dagelijkse data
    └── snap_YYYY-MM-DD.json
```

---

## 🎨 Features

### Responsive Design
- ✅ **Mobile First** - Geoptimaliseerd voor mobiel
- ✅ **Tablet Support** - Perfect op iPad
- ✅ **Desktop Ready** - Volledige ervaring
- ✅ **Touch Friendly** - Werkt met touchscreen

### Dark/Light Mode
- ✅ Automatische detectie
- ✅ Toggle in header
- ✅ Opgeslagen voorkeur

### Zoekfunctie
- ✅ Zoek op ticker, sector, signal
- ✅ Real-time filtering
- ✅ Keyboard support

### Table Filters
- ✅ Filter op Koop/Neutraal/Verkoop
- ✅ Sorteer op elke kolom
- ✅ Responsive table

---

## ⚙️ Configuratie

### Aandelen Aanpassen

Edit `stock_analyzer.py`:

```python
TICKERS = [
    'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META',
    'AMD', 'INTC', 'TSM', 'AVGO', 'QCOM', 'TXN',
    'TSLA', 'RIVN', 'LCID', 'F', 'GM',
    # ... voeg toe wat je wilt
]
```

### Workflow Timing

Edit `.github/workflows/main.yml`:

```yaml
on:
  schedule:
    - cron: '30 6 * * 1-5'  # Ma-vr 06:30 UTC
```

**Tijdzones:**
- 06:30 UTC = 07:30 CET (Nederland/België)
- 06:30 UTC = 01:30 EST (New York)

---

## 🛠️ Technologies (Allemaal Gratis!)

| Component | Technologie | Kosten |
|-----------|-------------|--------|
| Backend | Python 3.11+ | 🆓 Gratis |
| Data | yfinance | 🆓 Gratis |
| Nieuws | Yahoo Finance + RSS | 🆓 Gratis |
| Sentiment | Keyword analysis | 🆓 Gratis |
| Frontend | HTML5, CSS3, JS | 🆓 Gratis |
| Hosting | GitHub Pages | 🆓 Gratis |
| Automation | GitHub Actions | 🆓 Gratis |

**Totaal:** €0,00 per maand!

---

## 📊 Signal Betekenissen

| Signal | Betekenis | Criteria |
|--------|-----------|----------|
| 🟢 **Sterk Koop** | Sterke bullische setup | Score ≥4 + upside ≥5% |
| 🟢 **Koop** | Bullische setup | Score ≥2 + upside ≥4% |
| ⚪ **Neutraal** | Geen duidelijk signaal | Score 0-2 |
| 🔴 **Voorzichtig** | Bearish waarschuwing | Score -2 tot 0 |
| 🔴 **Verkoop** | Bearish setup | Score <-2 |

---

## 📱 Responsive Breakpoints

| Device | Width | Layout |
|--------|-------|--------|
| Desktop | >1024px | Volledig menu |
| Tablet | ≤1024px | Hamburger menu |
| Mobile | ≤640px | Compact layout |
| Small | ≤380px | Minimal |

---

## 🔧 Troubleshooting

### "No data found" voor bepaalde tickers
- Sommige tickers zijn mogelijk delisted
- Check ticker symbol (ASML.AS voor Amsterdam)
- Yahoo Finance heeft soms rate limits

### Workflow wordt niet uitgevoerd
- Check Actions tab voor errors
- Verify GitHub Pages staat aan
- Forceer handmatige run

### Sentiment lijkt niet te werken
- Keyword analyse is eenvoudig (geen AI)
- Werkt het beste met Engels nieuws
- Score is indicatief

---

## 📝 Wat Je Krijgt

Elke ochtend automatisch:

1. **Homepage** met:
   - Markt overzicht (75+ aandelen)
   - Top picks met analyse
   - Stats en filters
   - Zoekfunctie

2. **Data exports**:
   - Ruwe data (JSON)
   - Zoek index
   - Historische snapshots

3. **Volledig responsive**:
   - Werkt op mobiel
   - Tablet optimalisatie
   - Desktop ervaring

---

## 🎯 Next Steps

1. ✅ Clonen: `git clone ...`
2. ✅ Installeren: `pip install -r requirements.txt`
3. ✅ Testen: `python stock_analyzer.py`
4. ✅ GitHub Pages aan (optioneel)
5. ✅ Genieten maar! 🤠

---

## 🏆 Roadmap

- [ ] Meer RSS feeds toevoegen
- [ ] Portfolio tracking
- [ ] Price alerts (email)
- [ ] Backtesting module
- [ ] Meerdere talen

---

## 🤠 Over de Naam

"Beurs Cowboy" omdat:
- Trading net het wilde westen kan zijn
- Je soms een sheriff nodig hebt
- Het leuk klinkt
- Yeehaw! 🤠

---

## 💰 Kosten Overzicht

| Dienst | Kosten |
|--------|--------|
| Python | €0,00 |
| yfinance | €0,00 |
| GitHub Pages | €0,00 |
| GitHub Actions | €0,00 |
| **TOTAAL** | **€0,00** |

Geen credit card nodig. Geen "free trial" die na 30 dagen €50 kost. Gewoon gratis.

---

*Beurs Cowboy - Dagelijkse beursanalyse, vers van de pers.*

*Data: Yahoo Finance | Nieuws: RSS Feeds | Hosting: GitHub Pages | Wijsheid: Het Wilde Westen*
