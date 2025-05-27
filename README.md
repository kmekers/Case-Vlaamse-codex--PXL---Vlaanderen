# 🦁 Vlaamse Codex Project - PXL Business Architect AI

Repo van onze case. Notebook die de hele codex inhaalt, agent en prototype (mock ups) ontwikkeld voor de PXL Business Architect AI opleiding.
Teamleden: Koen, Charlotte en Elke
Coach: Tim

## 📋 Project Overzicht

Dit project bestaat uit drie hoofdcomponenten:

### 1. 🤖 AI Agent (`Agent V2/`)
Een Python Flask-gebaseerde AI agent die drukproef documenten analyseert met Claude Sonnet 4.

**Functionaliteiten:**
- Automatische analyse van drukproef documenten
- Vergelijking met officiële Vlaamse Codex database
- Real-time logging en status updates
- Web-gebaseerde interface

**Snelle start:**
```bash
cd "Agent V2/Agent V2"
pip install -r requirements.txt
python app.py
# Ga naar http://127.0.0.1:5000
```

### 2. 📊 Data Scraper (`notebook/`)
Jupyter notebook voor het scrapen en analyseren van de Vlaamse Codex via de officiële API.

**Functionaliteiten:**
- API scraping van Vlaamse Codex documenten
- HTML naar Markdown conversie
- Data analyse en visualisaties
- Georganiseerde document structuur

**Snelle start:**
```bash
cd notebook
pip install -r requirements.txt
jupyter notebook
# Open Vlaamsecodexcase.ipynb
```

### 3. 🎨 Frontend Prototype (`frontendprototype/`)
Een statische mockup van de gebruikersinterface voor de Vlaamse Codex applicatie.

**Functionaliteiten:**
- Dashboard met overzicht van wijzigingen
- AI Consolidatie interface
- Staatsblad monitoring
- Geschiedenis en instellingen

**Snelle start:**
```bash
cd frontendprototype
# Open index.html in je browser
# Of bekijk online: https://kmekers.github.io
```

## 🚀 Volledige Setup

### Vereisten
- Python 3.8+
- pip
- Jupyter Notebook (voor data scraper)
- Moderne webbrowser

### Installatie Stappen

1. **Clone het project:**
   ```bash
   git clone [repository-url]
   cd Case-Vlaamse-codex--PXL---Vlaanderen
   ```

2. **Setup AI Agent:**
   ```bash
   cd "Agent V2/Agent V2"
   pip install -r requirements.txt
   # Voeg ANTHROPIC_API_KEY toe aan .env
   python app.py
   ```

3. **Setup Data Scraper:**
   ```bash
   cd notebook
   pip install -r requirements.txt
   jupyter notebook
   ```

4. **Bekijk Frontend:**
   ```bash
   cd frontendprototype
   # Open index.html of ga naar https://kmekers.github.io
   ```

## 🔧 Technische Stack

- **Backend**: Python, Flask, Anthropic Claude API
- **Data Processing**: Jupyter, Pandas, MarkItDown
- **Frontend**: HTML, CSS, JavaScript, Font Awesome
- **AI**: Claude Sonnet 4, Gemini 2.0 Flash (geplanned)
- **APIs**: Vlaamse Codex officiële API

## 📁 Project Structuur

```
Case-Vlaamse-codex--PXL---Vlaanderen/
├── Agent V2/                    # AI Agent applicatie
│   └── Agent V2/
│       ├── app.py              # Flask server
│       ├── vlaamsecodexagent.py # Agent logica
│       ├── tools/              # Agent tools
│       └── requirements.txt
├── notebook/                   # Data scraper & analyse
│   ├── Vlaamsecodexcase.ipynb # Hoofdnotebook
│   ├── codexjson/             # Ruwe API data
│   ├── organized_documents_v3/ # Verwerkte documenten
│   └── requirements.txt
├── frontendprototype/          # UI mockup
│   ├── index.html             # Dashboard
│   ├── pages/                 # Verschillende pagina's
│   ├── css/                   # Styling
│   └── js/                    # JavaScript
└── README.md                  # Dit bestand
```

## 🎯 Gebruik Cases

1. **Wetgeving Analyse**: Upload drukproef documenten voor automatische analyse
2. **Data Mining**: Scrape en analyseer Vlaamse Codex voor trends
3. **UI/UX Design**: Bekijk en test de gebruikersinterface
4. **Research**: Gebruik voor academische doeleinden en AI training

## ⚠️ Belangrijke Opmerkingen

- **Eerste Jupyter Project & agent**: Dit is mijn eerste Jupyter notebook project - er kunnen kinderziektes zijn
- **Prototype Status**: Frontend is een mockup zonder werkende backend
- **API Keys**: Vergeet niet je Anthropic API key toe te voegen voor de agent
- **Desktop Focus**: Frontend is geoptimaliseerd voor desktop gebruik

## 🔗 Links

- **Live Frontend**: [https://kmekers.github.io](https://github.com/kmekers/kmekers.github.io)
- **LinkedIn**: [Koen Mekers](https://www.linkedin.com/in/koen-mekers-a350b018a/)
- **Vlaamse Codex**: [Officiële website](https://codex.vlaanderen.be/)

## 📞 Contact

Voor vragen of problemen, neem contact op via LinkedIn (Koen Mekers)

---

*Ontwikkeld voor de PXL Business Architect AI opleiding* 🎓 
