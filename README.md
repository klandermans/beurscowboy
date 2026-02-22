# 🤠 Beurs Cowboy

**Dagelijkse beursanalyse met een westelijk tintje**

> "Trading is als het wilde westen - er zijn schurken en er zijn sheriffs. Wees een sheriff."

---

## Over Beurs Cowboy

Beurs Cowboy is een geautomatiseerd platform dat dagelijks marktanalyses genereert met:

- 📊 **Technische Analyse** - RSI, MACD, Moving Averages, ATR
- 🧠 **AI Sentiment** - Qwen LLM analyseert nieuwsartikelen
- 🎯 **Trading Signals** - Koop/Verkoop aanbevelingen met scores
- 📱 **Volledig Responsive** - Werkt perfect op mobiel, tablet en desktop
- 🌓 **Dark Mode** - Oogvriendelijk voor lange sessies
- 🔍 **Zoekfunctie** - Snel aandelen vinden
- 🤠 **Westelijke Charme** - Want trading moet ook leuk blijven

---

## ⚠️ Disclaimer

**Dit is GEEN financieel advies.**

- Trading in aandelen brengt significante risico's met zich mee
- Dit platform is voor educatieve en informatieve doeleinden
- Raadpleeg een licensed financial advisor voor persoonlijk advies
- Trade nooit met geld dat je niet kunt verliezen
- De volgende black swan wordt waarschijnlijk getraind op een GPU cluster

---

## 🚀 Quick Start

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

### 3. API Key Instellen

**DashScope API Key aanvragen:**
1. Ga naar [Alibaba Cloud DashScope](https://dashscope.console.aliyun.com/)
2. Maak account aan
3. Kopieer API key

**Environment variable:**
```bash
export DASHSCOPE_API_KEY=sk-jouw-api-key
```

### 4. Lokaal Testen

```bash
python stock_analyzer.py
```

Open `docs/index.html` in je browser.

---

## 🌐 GitHub Pages Setup

### Stap 1: Enable GitHub Pages

1. Ga naar **Settings** → **Pages**
2. Bij "Source": Kies **Deploy from a branch**
3. Branch: **main** → Folder: **/docs**
4. Klik **Save**

### Stap 2: API Key als Secret Toevoegen

1. Ga naar **Settings** → **Secrets and variables** → **Actions**
2. Klik **New repository secret**
3. Naam: `DASHSCOPE_API_KEY`
4. Value: jouw API key
5. Klik **Add secret**

### Stap 3: Workflow Testen

1. Ga naar **Actions** → **Daily Market Analysis**
2. Klik **Run workflow**
3. Wacht tot de workflow klaar is (~2-3 minuten)

### Stap 4: Site Bekijken

Je site is nu beschikbaar op:
```
https://jouw-username.github.io/jouw-repo/
```

---

## 📁 Bestandsstructuur

```
stockker/
├── stock_analyzer.py          # Main analysis script
├── requirements.txt           # Python dependencies
├── README.md                  # Deze handleiding
├── .env.example              # Environment template
├── .github/workflows/
│   └── main.yml              # GitHub Actions workflow
├── docs/                      # Website (wordt gehost op GitHub Pages)
│   ├── index.html            # Homepage
│   ├── analysis.html         # Analyse pagina
│   ├── watchlist.html        # Watchlist pagina
│   ├── archive.html          # Archief pagina
│   ├── article/              # Dagelijkse artikelen
│   │   └── YYYY-MM-DD.html
│   └── assets/
│       ├── styles.css        # Styling met dark mode & responsive
│       └── main.js           # Interactive features
└── data_snapshots/           # Dagelijkse data exports
    └── snap_YYYY-MM-DD.json
```

---

## 🎨 Features

### Responsive Design
- **Mobile First** - Geoptimaliseerd voor mobiel
- **Tablet Support** - Perfect op iPad en tablets
- **Desktop Ready** - Volledige ervaring op desktop
- **Touch Friendly** - Werkt great met touchscreens

### Dark/Light Mode
- Automatische theme detectie
- Toggle knop in header
- Opgeslagen voorkeur in localStorage
- Volgt systeem voorkeur

### Zoekfunctie
- Zoek op ticker, sector, of signal
- Real-time filtering
- Escape to sluiten
- Keyboard support

### Table Filters
- Filter op Koop/Neutraal/Verkoop signals
- Sorteer op elke kolom (klik op header)
- Responsive table met horizontal scroll
- Keyboard accessible

### Mobile Menu
- Hamburger menu op mobiel
- Smooth animaties
- Sluit bij klik buiten menu
- Scroll lock wanneer open

---

## ⚙️ Configuratie

### Aandelen Aanpassen

Edit `stock_analyzer.py`:

```python
TICKERS = [
    # Mega Cap Tech
    'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META',
    # Semiconductors
    'AMD', 'INTC', 'TSM', 'AVGO', 'QCOM', 'TXN',
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
- 06:30 UTC = 14:30 JST (Tokyo)

---

## 🛠️ Technologies

| Component | Technologie |
|-----------|-------------|
| Backend | Python 3.11+ |
| Data | yfinance, pandas, numpy |
| AI/LLM | Qwen Agent (DashScope) |
| Frontend | HTML5, CSS3, Vanilla JS |
| Design | Custom (Beurs Cowboy theme) |
| Hosting | GitHub Pages |
| Automation | GitHub Actions |

---

## 📊 Signal Betekenissen

| Signal | Betekenis | Score |
|--------|-----------|-------|
| 🟢 **Sterk Koop** | Sterke bullische setup | ≥4 + upside ≥5% |
| 🟢 **Koop** | Bullische setup | ≥2 + upside ≥4% |
| ⚪ **Neutraal** | Geen duidelijk signaal | 0 tot 2 |
| 🔴 **Voorzichtig** | Bearish waarschuwing | -2 tot 0 |
| 🔴 **Verkoop** | Bearish setup | <-2 |

---

## 📱 Responsive Breakpoints

| Device | Width | Features |
|--------|-------|----------|
| Desktop | >1024px | Volledig menu, alle stats |
| Tablet | ≤1024px | Hamburger menu, 2 koloms stats |
| Mobile | ≤640px | Compact menu, 1 kolom layout |
| Small Mobile | ≤380px | Minimal layout, logo only |

---

## 🔧 Troubleshooting

### Workflow faalt met "API Key Error"
- Check of `DASHSCOPE_API_KEY` correct is ingesteld
- Verify API key is actief op dashscope.console.aliyun.com
- Check credits op je DashScope account

### "No data found" voor bepaalde tickers
- Sommige tickers zijn mogelijk delisted
- Check ticker symbol (bijv. ASML.AS voor Amsterdam)
- Yahoo Finance heeft soms rate limits

### Site wordt niet geüpdatet
- Check GitHub Actions logs voor errors
- Verify GitHub Pages is ingesteld op /docs folder
- Forceer een handmatige workflow run

### Mobile menu werkt niet
- Hard refresh (Ctrl+Shift+R / Cmd+Shift+R)
- Check browser console voor errors
- Clear cache en cookies

---

## 📝 Dagelijkse Output

Elke run genereert:

1. **Homepage Update** (`docs/index.html`)
   - Markt overzicht met alle aandelen
   - Top picks met gedetailleerde cards
   - Statistieken en filters
   - Volledig responsive

2. **Data Snapshot** (`data_snapshots/snap_YYYY-MM-DD.json`)
   - Ruwe data voor alle aandelen
   - Handig voor eigen analyse

3. **Zoek Index** (`docs/search-index.json`)
   - Index voor zoekfunctie
   - Snel vinden van aandelen

---

## 🎯 Next Steps

1. ✅ API Key aanvragen bij DashScope
2. ✅ Lokaal testen met `python stock_analyzer.py`
3. ✅ GitHub Pages instellen
4. ✅ DASHSCOPE_API_KEY secret toevoegen
5. ✅ Workflow handmatig triggeren om te testen
6. ✅ Genieten van je dagelijkse marktanalyse!

---

## 🏆 Features Roadmap

- [ ] Real-time prijs updates
- [ ] Portfolio tracking
- [ ] Price alerts via email
- [ ] Backtesting module
- [ ] Meerdere taalondersteuning
- [ ] API endpoint voor externe toegang

---

## 📞 Support

Voor vragen of issues:
- Check de [GitHub Issues](https://github.com/jouw-username/stockker/issues)
- Lees de troubleshooting sectie hierboven

---

## 🤠 Over de Naam

"Beurs Cowboy" omdat:
- Trading net het wilde westen kan zijn
- Je soms een sheriff nodig hebt (onze AI)
- Het leuk klinkt
- Yeehaw! 🤠

---

*Beurs Cowboy - Dagelijkse beursanalyse, vers van de pers.*

*Data: Yahoo Finance | Sentiment: Qwen LLM | Hosting: GitHub Pages | Wijsheid: Het Wilde Westen*
