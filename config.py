"""
Beurs Cowboy - Configuration

Centrale configuratie voor het Beurs Cowboy project.
Gescheiden van business logic voor betere maintainability.
"""

# =============================================================================
# SENTIMENT KEYWORDS
# =============================================================================

SENTIMENT_KEYWORDS = {
    'positive': [
        'stijgt', 'stijging', 'winst', 'groei', 'record', 'bullish', 'koop',
        'beat', 'outperforms', 'upgrade', 'positive', 'strong', 'growth',
        'surge', 'rally', 'gain', 'profit', 'success', 'breakthrough',
        'optimistic', 'outlook', 'exceeds', 'expectations', 'koopadvies',
        'verwacht', 'positief', 'hoog', 'beter', 'goed', 'nieuwe',
        'lanceert', 'partnership', 'deal', 'contract', 'wint'
    ],
    'negative': [
        'daalt', 'daling', 'verlies', 'crash', 'bearish', 'verkoop',
        'miss', 'underperforms', 'downgrade', 'negative', 'weak', 'decline',
        'drop', 'fall', 'loss', 'failure', 'lawsuit', 'investigation',
        'pessimistic', 'warning', 'below', 'expectations', 'verkoopadvies',
        'risico', 'negatief', 'laag', 'slechter', 'probleem', 'rechtszaak',
        'onderzoek', 'boete', 'terugroep', 'storing', 'fout'
    ]
}

MACRO_KEYWORDS = {
    'positive': [
        'growth', 'expansion', 'recovery', 'boom', 'rally', 'surge', 'gain',
        'positive', 'optimistic', 'beat', 'exceeds', 'upgrade', 'stimulus',
        'koop', 'winst', 'stijging', 'groei', 'positief', 'beter'
    ],
    'negative': [
        'recession', 'crisis', 'crash', 'decline', 'slowdown', 'warning',
        'negative', 'pessimistic', 'miss', 'downgrade', 'inflation', 'rate hike',
        'verkoop', 'verlies', 'daling', 'negatief', 'slechter', 'risico'
    ]
}

# =============================================================================
# RSS FEEDS
# =============================================================================

RSS_FEEDS = {
    # Noord-Amerika
    'marketwatch': 'https://feeds.marketwatch.com/marketwatch/topstories/',
    'reuters_business': 'https://www.reutersagency.com/feed/',
    'yahoo_finance': 'https://finance.yahoo.com/news/rssindex',
    'bloomberg_markets': 'https://feeds.bloomberg.com/markets/news.rss',
    'cnbc_top_news': 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114',
    'seeking_alpha': 'https://seekingalpha.com/feed.xml',
    'benzinga': 'https://www.benzinga.com/news/feed',
    'barrons': 'https://www.barrons.com/xml/rss/',
    'motley_fool': 'https://www.fool.com/feeds/latest/',
    
    # Europa
    'financial_times': 'https://www.ft.com/?format=rss',
    'reuters_uk': 'https://www.reutersagency.com/feed/?post_type=best&taxonomy=topic&term=uk',
    'handelsblatt': 'https://www.handelsblatt.com/content/feed/rss',
    'les_echos': 'https://www.lesechos.fr/finance-medias/rss',
    'il_sole_24_ore': 'https://www.ilsole24ore.com/rss/italia.xml',
    'expansion': 'https://www.expansion.com/rss/economia.html',
    
    # Azië - China
    'china_daily': 'http://www.chinadaily.com.cn/rss/business.xml',
    'scmp_business': 'https://www.scmp.com/rss/311643/feed',
    'xinhua_business': 'http://www.xinhuanet.com/english/rss/businessrss.xml',
    'caixin': 'https://www.caixinglobal.com/rss/',
    
    # Azië - Japan
    'nikkei_asia': 'https://asia.nikkei.com/rss',
    'japan_times': 'https://www.japantimes.co.jp/feed/',
    'nhk_world': 'https://www3.nhk.or.jp/nhkworld/en/news/rss/',
    
    # Azië - Overig
    'korea_herald': 'http://www.koreaherald.com/common/rss_xml.php?mt=business',
    'korea_times': 'https://www.koreatimes.co.kr/rss/business',
    'straits_times': 'https://www.straitstimes.com/rss/singapore-business-news',
    'bangkok_post': 'https://www.bangkokpost.com/rss/business',
    
    # Australië & Oceanië
    'australian_financial_review': 'https://www.afr.com/rss',
    'abc_news_au': 'https://www.abc.net.au/news/feed/46182/rss.xml',
    'sydney_morning_herald': 'https://www.smh.com.au/rss/feed/business.xml',
    'nz_herald': 'https://www.nzherald.co.nz/arc/outboundfeeds/rss/section/business/',
    
    # Midden-Oosten
    'arabian_business': 'https://www.arabianbusiness.com/politics-economics',
    'gulf_news': 'https://www.gulfnews.com/business/1.1028906?rssFeed=1',
    
    # Afrika
    'business_day_live': 'https://www.businesslive.co.za/bd/rss/',
    'fin24': 'https://www.fin24.com/rss',
    
    # Latijns-Amerika
    'valor_economico': 'https://valor.globo.com/rss/',
    'el_economista': 'https://www.eleconomista.com.mx/rss',
    
    # Tech & Crypto
    'tech_crunch': 'https://techcrunch.com/feed/',
    'coindesk': 'https://www.coindesk.com/arc/outboundfeeds/rss/',
    'cointelegraph': 'https://cointelegraph.com/rss',
}

REGIONAL_FEEDS = {
    'Noord-Amerika': ['marketwatch', 'reuters_business', 'yahoo_finance', 'bloomberg_markets', 'cnbc_top_news', 'seeking_alpha', 'benzinga', 'barrons', 'motley_fool'],
    'Europa': ['financial_times', 'reuters_uk', 'handelsblatt', 'les_echos', 'il_sole_24_ore', 'expansion'],
    'China': ['china_daily', 'scmp_business', 'xinhua_business', 'caixin'],
    'Japan': ['nikkei_asia', 'japan_times', 'nhk_world'],
    'Azië (Overig)': ['korea_herald', 'korea_times', 'straits_times', 'bangkok_post'],
    'Australië & Oceanië': ['australian_financial_review', 'abc_news_au', 'sydney_morning_herald', 'nz_herald'],
    'Midden-Oosten': ['arabian_business', 'gulf_news'],
    'Afrika': ['business_day_live', 'fin24'],
    'Latijns-Amerika': ['valor_economico', 'el_economista'],
    'Tech & Crypto': ['tech_crunch', 'coindesk', 'cointelegraph'],
}

# =============================================================================
# TECHNICAL ANALYSIS PARAMETERS
# =============================================================================

TECHNICAL_PARAMS = {
    'rsi_window': 14,
    'macd_fast': 12,
    'macd_slow': 26,
    'macd_signal': 9,
    'atr_period': 14,
    'volatility_period': 252,
    'sma_short': 20,
    'sma_medium': 50,
}

# =============================================================================
# SCORING WEIGHTS
# =============================================================================

SCORING_WEIGHTS = {
    'rsi_oversold': 2.0,
    'rsi_bullish': 1.5,
    'macd_bullish': 2.0,
    'ma_alignment': 2.0,
    'high_volatility': 1.0,
    'sentiment_multiplier': 3.0,
    'stocktwits_max_bonus': 0.3,
}

# =============================================================================
# STOCK TICKERS
# =============================================================================

TICKERS = [
    # Mega Cap Tech
    'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META',
    # Semiconductors
    'AMD', 'INTC', 'TSM', 'AVGO', 'QCOM', 'TXN',
    # EV & Auto
    'TSLA', 'RIVN', 'LCID', 'F', 'GM',
    # Tech / Software
    'ORCL', 'CRM', 'ADBE', 'NOW', 'INTU', 'PLTR',
    # Social / Media
    'NFLX', 'DIS', 'CMCSA', 'WBD',
    # Finance - Banks
    'JPM', 'BAC', 'GS', 'MS', 'WFC', 'C',
    # Finance - Payments
    'V', 'MA', 'PYPL', 'AFRM',
    # Finance - Crypto
    'COIN', 'MARA', 'RIOT', 'CLSK', 'HUT',
    # Retail
    'WMT', 'TGT', 'COST', 'HD', 'NKE', 'SBUX',
    # Healthcare - Big Pharma
    'JNJ', 'UNH', 'PFE', 'MRNA', 'REGN', 'GILD',
    # Energy
    'XOM', 'CVX', 'COP', 'SLB', 'OXY',
    # Industrials
    'CAT', 'BA', 'GE', 'HON', 'UPS',
    # European
    'ASML.AS', 'SAP', 'NESN.SW', 'NOVN.SW', 'AZN',
    # Cloud / Cybersecurity
    'SNOW', 'NET', 'DDOG', 'ZS', 'CRWD', 'MDB',
    # Biotech
    'BIIB', 'VRTX', 'ALNY', 'BMRN', 'INCY', 'TECH',
    # Real Estate
    'AMT', 'PLD', 'CCI', 'EQIX', 'SPG',
    # Telecom
    'T', 'VZ', 'TMUS', 'CHTR',
    # Consumer Discretionary
    'MCD', 'LULU', 'DECK', 'CROX',
    # Airlines
    'DAL', 'UAL', 'AAL', 'LUV',
    # Cruise Lines
    'CCL', 'RCL', 'NCLH',
    # Gaming
    'DKNG', 'PENN', 'MGM', 'WYNN',
    # Cannabis
    'TLRY', 'SNDL', 'CGC', 'ACB',
    # China Tech
    'BABA', 'JD', 'PDD', 'BIDU', 'NIO',
    # Small Cap Growth
    'UPST', 'SOFI', 'HOOD', 'RBLX', 'U', 'PATH',
    # Dividend Kings
    'KO', 'PEP', 'PG', 'MMM', 'JNJ',
    # Utilities
    'NEE', 'DUK', 'SO', 'D',
    # Materials
    'LIN', 'APD', 'ECL', 'SHW',
    # Defense
    'LMT', 'RTX', 'NOC', 'GD',
]

# =============================================================================
# COMPANY NAMES & SECTORS
# =============================================================================

COMPANY_NAMES = {
    'AAPL': 'Apple Inc', 'MSFT': 'Microsoft Corporation', 'NVDA': 'NVIDIA Corporation',
    'GOOGL': 'Alphabet Inc', 'AMZN': 'Amazon.com Inc', 'META': 'Meta Platforms',
    'AMD': 'Advanced Micro Devices', 'INTC': 'Intel Corporation', 'TSM': 'TSMC',
    'AVGO': 'Broadcom Inc', 'QCOM': 'Qualcomm Inc', 'TXN': 'Texas Instruments',
    'TSLA': 'Tesla Inc', 'RIVN': 'Rivian Automotive', 'LCID': 'Lucid Group',
    'F': 'Ford Motor', 'GM': 'General Motors',
    'ORCL': 'Oracle Corporation', 'CRM': 'Salesforce Inc', 'ADBE': 'Adobe Inc',
    'NOW': 'ServiceNow Inc', 'INTU': 'Intuit Inc', 'PLTR': 'Palantir Technologies',
    'NFLX': 'Netflix Inc', 'DIS': 'Walt Disney Co', 'CMCSA': 'Comcast Corp',
    'WBD': 'Warner Bros Discovery',
    'JPM': 'JPMorgan Chase', 'BAC': 'Bank of America', 'GS': 'Goldman Sachs',
    'MS': 'Morgan Stanley', 'WFC': 'Wells Fargo', 'C': 'Citigroup',
    'COIN': 'Coinbase Global', 'MARA': 'Marathon Digital', 'RIOT': 'Riot Platforms',
    'CLSK': 'CleanSpark Inc', 'HUT': 'Hut 8 Mining',
    'V': 'Visa Inc', 'MA': 'Mastercard Inc', 'PYPL': 'PayPal Holdings',
    'AFRM': 'Affirm Holdings',
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
    'CROX': 'Crocs Inc',
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
    'GD': 'General Dynamics',
}

SECTORS = {
    'AAPL': 'Technologie', 'MSFT': 'Technologie', 'NVDA': 'Technologie',
    'GOOGL': 'Technologie', 'AMZN': 'Consument', 'META': 'Technologie',
    'AMD': 'Technologie', 'INTC': 'Technologie', 'TSM': 'Technologie',
    'AVGO': 'Technologie', 'QCOM': 'Technologie', 'TXN': 'Technologie',
    'TSLA': 'Automotive', 'RIVN': 'Automotive', 'LCID': 'Automotive',
    'F': 'Automotive', 'GM': 'Automotive',
    'ORCL': 'Technologie', 'CRM': 'Technologie', 'ADBE': 'Technologie',
    'NOW': 'Technologie', 'INTU': 'Technologie', 'PLTR': 'Technologie',
    'NFLX': 'Communicatie', 'DIS': 'Communicatie', 'CMCSA': 'Communicatie',
    'WBD': 'Communicatie',
    'JPM': 'Financieel', 'BAC': 'Financieel', 'GS': 'Financieel',
    'MS': 'Financieel', 'WFC': 'Financieel', 'C': 'Financieel',
    'COIN': 'Financieel', 'MARA': 'Financieel', 'RIOT': 'Financieel',
    'CLSK': 'Financieel', 'HUT': 'Financieel',
    'V': 'Financieel', 'MA': 'Financieel', 'PYPL': 'Financieel',
    'AFRM': 'Financieel',
    'WMT': 'Consument', 'TGT': 'Consument', 'COST': 'Consument',
    'HD': 'Consument', 'NKE': 'Consument', 'SBUX': 'Consument',
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
    'CROX': 'Consument',
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
    'GD': 'Defensie',
}

# =============================================================================
# APPLICATION SETTINGS
# =============================================================================

SETTINGS = {
    'output_dir': 'docs',
    'data_dir': 'data_snapshots',
    'archive_dir': 'docs/archive',
    'rss_feed_limit': 25,
    'max_age_hours': 24,
    'max_headlines_per_ticker': 10,
    'max_llm_headlines': 7,
    'max_trending_display': 5,
    'max_regional_display': 8,
    'parallel_workers': 10,
}
