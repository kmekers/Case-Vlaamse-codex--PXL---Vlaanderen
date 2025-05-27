# Vlaamse Codex Scraper

## Beschrijving
Dit project bevat een Jupyter notebook voor het scrapen en analyseren van de Vlaamse Codex. Het notebook haalt wetgevingsdocumenten op via de officiële API, converteert HTML naar Markdown, en voert verschillende analyses uit op de data.

## ⚠️ Belangrijke Opmerking
**Dit is mijn eerste keer dat ik een Jupyter notebook maak en op GitHub zet!** Er kunnen dus zeker nog wat kinderziektes in zitten. Als je problemen ondervindt bij de installatie of het uitvoeren van de code, dan ligt het waarschijnlijk aan mijn onervaring en niet aan jou 😅

## Installatie

### Vereisten
- Python 3.8 of hoger
- pip (Python package manager)

### Stappen
1. Clone deze repository:

git clone [repository-url]
cd vlaamsecodexfinal


2. Installeer de vereiste packages:

pip install -r requirements.txt


3. Start Jupyter Notebook:

jupyter notebook


4. Open `Vlaamsecodexcase.ipynb`

## Wat doet dit project?

### Hoofdfuncties:
- **API Scraping**: Haalt documenten op van de Vlaamse Codex API + sorteren & dieper ingaan op decreten
- **HTML naar Markdown conversie**: Gebruikt Microsoft's MarkItDown library
- **Data analyse**: Visualisaties en trends over wetgeving
- **Tekst opschoning**: Automatische formatting van artikelen

### Mappenstructuur:
- `codexjson/` - Ruwe JSON data van de API
- `organized_documents_v3/` - Georganiseerde documenten per type
- `reports/` - Analyse rapporten
- `Vlaamsecodexcase.ipynb` - De hoofdnotebook

## Mogelijke Problemen
Er problemen optreden met:
- Package versies die niet compatibel zijn
- Ontbrekende dependencies
- Pad-gerelateerde fouten
- MarkItDown installatie issues

Als je problemen hebt, probeer dan:
1. Een virtual environment te gebruiken
2. Package versies te updaten: `pip install --upgrade [package-naam]`
3. Voor MarkItDown specifiek: `pip install markitdown[all]`

## Contact
Als je vragen hebt of problemen ondervindt, aarzel niet om contact op te nemen. 
Linkedin: https://www.linkedin.com/in/koen-mekers-a350b018a/

*Gemaakt voor de PXL Business Architect AI opleiding* 