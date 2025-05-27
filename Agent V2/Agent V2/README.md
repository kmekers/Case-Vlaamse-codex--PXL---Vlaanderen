# 🦁 Vlaamse Codex AgentEen Python en flask-gebaseerde AI agent voor het analyseren van Vlaamse drukproef documenten met behulp van Claude Sonnet 4.

## 🚀 Snelle Start 

### Vereisten
- Python 3.8+
- pip

### Installatie

1. **Installeer dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start de Flask server:**
   ```bash
   python app.py
   ```

3. **Open je browser:**
   Ga naar `http://127.0.0.1:5000`

## 🤖 Agent Overzicht

De Vlaamse Codex Agent is een AI-gestuurde assistent die drukproef documenten analyseert en vergelijkt met de officiële Vlaamse wetgeving. De agent gebruikt Claude Sonnet 4 en heeft toegang tot verschillende gespecialiseerde tools.

### 🛠️ Beschikbare Tools

1. **`zoek_vlaamse_codex_api`** - Zoekt in de officiële Vlaamse Codex database
   - Vindt relevante wetgeving en decreten
   - Ondersteunt zoeken op trefwoorden en artikelnummers

2. **`vind_relatie`** - Analyseert relaties tussen documenten
   - Identificeert verbanden tussen drukproef en bestaande wetgeving
   - Detecteert wijzigingen en aanpassingen

3. **`krijg_voorlaatste_versie`** - Haalt vorige versies van documenten op
   - Vergelijkt met eerdere versies
   - Toont evolutie van wetgeving

4. **`krijg_beschikbare_tools`** - Toont beschikbare functionaliteit
   - Dynamische tool discovery
   - Helpt bij troubleshooting

### 🔍 Analyse Proces

1. **Document Inlezen** - Leest `drukproef.md` in
2. **Wetgeving Zoeken** - Zoekt relevante artikelen in Vlaamse Codex
3. **Vergelijking** - Analyseert verschillen en overeenkomsten
4. **Relatie Mapping** - Identificeert juridische verbanden
5. **Rapport Generatie** - Produceert gedetailleerde analyse

## 📁 Project Structuur

```
vlaamsecodexagent/
├── app.py                 # Flask server (NIEUW)
├── requirements.txt       # Python dependencies (NIEUW)
├── drukproef.md          # Drukproef document om te analyseren
├── Agent V2/             # Frontend en agent code
│   ├── index.html        # Hoofdpagina
│   ├── styles.css        # Styling
│   ├── script.js         # Frontend JavaScript
│   ├── vlaamsecodexagent.py  # Agent logica
│   └── tools/            # Agent tools
│       ├── __init__.py
│       ├── krijg_beschikbare_tools.py
│       ├── krijg_voorlaatste_versie.py
│       ├── vind_relatie.py
│       └── zoek_vlaamse_codex_api.py
└── README.md             # Dit bestand (NIEUW)
```

## 🔧 API Endpoints

De Flask app biedt de volgende endpoints:

- `GET /` - Hoofdpagina (frontend)
- `POST /start` - Start drukproef analyse
- `GET /logs` - Krijg real-time logs
- `GET /status` - Krijg analyse status
- `GET /analysis` - Krijg analyse resultaten
- `GET /document/<id>` - Krijg specifiek document
- `GET /health` - Health check

## 🎯 Gebruik

1. **Start de server** met `python app.py`
2. **Open de webinterface** op `http://127.0.0.1:5000`
3. **Klik op "Start Analyse"** om de drukproef analyse te beginnen
4. **Bekijk real-time logs** in het modal venster
5. **Download resultaten** wanneer de analyse voltooid is

## 🛠️ Technische Details

### Frontend
- **HTML/CSS/JavaScript** - Moderne, responsive UI
- **Real-time updates** - Polling voor logs en status
- **Modal interface** - Volledige scherm analyse weergave

### Backend
- **Flask** - Python web framework
- **Threading** - Achtergrond analyse uitvoering
- **Log Capture** - Real-time log streaming
- **CORS** - Cross-origin resource sharing

### Agent
- **Claude Sonnet 4** - AI model voor analyse
- **Vlaamse Codex API** - Wetgeving database toegang
- **Tool-based architecture** - Modulaire functionaliteit

## 🔐 Beveiliging


```bash
# .env
ANTHROPIC_API_KEY=your_api_key_here
```

## 🐛 Troubleshooting

### Poort al in gebruik
Als poort 5000 al in gebruik is, wijzig de poort in `app.py`:
```python
app.run(debug=True, host='127.0.0.1', port=5001)  # Gebruik poort 5001
```

### Import errors
Zorg ervoor dat alle dependencies geïnstalleerd zijn:
```bash
pip install -r requirements.txt
```

### Agent errors
Controleer of `drukproef.md` bestaat in de root directory.

## 📝 Ontwikkeling

Voor ontwikkeling is debug mode ingeschakeld. De server herstart automatisch bij code wijzigingen.

## 🔄 Versie

- **v1.0.0** - Initiële Flask integratie met bestaande frontend en agent 