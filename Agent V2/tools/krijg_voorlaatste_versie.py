import requests
import urllib.parse
from typing import Dict, Any
from bs4 import BeautifulSoup
import re

def krijg_voorlaatste_versie(document_id: str, datum: str = "2024-05-01") -> Dict[str, Any]:
    """
    Krijg de HTML inhoud van een document van de Vlaanderen Codex website.
    
    Args:
        document_id (str): Het document ID om op te halen
        datum (str): De datum om een specifieke versie van het document op te halen (YYYY-MM-DD formaat). Gebruik een datum die VOOR de meest recente wijziging ligt om de voorlaatste (tweede meest recente) versie te krijgen, niet de allerlaatste of allereerste versie.
        
    Returns:
        Dict[str, Any]: De gescrapte inhoud en metadata
    """
    basis_url = "https://codex.vlaanderen.be/PrintDocument.ashx"
    params = {
        "id": document_id,
        "datum": datum,
        "geannoteerd": "false",
        "print": "false"
    }
    
    # Construeer de volledige URL
    url = f"{basis_url}?" + urllib.parse.urlencode(params)
    
    try:
        # Maak de request met headers om een browser na te bootsen
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise een exception voor slechte status codes
        
        # Parse de HTML inhoud
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraheer de hoofdinhoud (verwijder scripts, styles, etc.)
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Krijg de ruwe tekstinhoud
        tekst_inhoud = soup.get_text()
        
        # STAP 1: Basis opschoning - verwijder overtollige witruimte
        lijnen = []
        for lijn in tekst_inhoud.splitlines():
            schone_lijn = lijn.strip()
            if schone_lijn:  # Behoud alleen niet-lege lijnen
                lijnen.append(schone_lijn)
        
        # STAP 2: Verwijder dubbele opeenvolgende lijnen
        gededupliceerde_lijnen = []
        vorige_lijn = None
        for lijn in lijnen:
            if lijn != vorige_lijn:
                gededupliceerde_lijnen.append(lijn)
            vorige_lijn = lijn
        
        # STAP 3: Voeg haakjes samen met vorige lijn en identificeer structuur
        gestructureerde_lijnen = []
        i = 0
        while i < len(gededupliceerde_lijnen):
            huidige_lijn = gededupliceerde_lijnen[i]
            
            # Controleer of volgende lijn haakjes zijn die samengevoegd moeten worden
            if (i + 1 < len(gededupliceerde_lijnen) and 
                gededupliceerde_lijnen[i + 1].startswith('(') and 
                gededupliceerde_lijnen[i + 1].endswith(')')):
                # Voeg samen met haakjes
                samengevoegde_lijn = f"{huidige_lijn} {gededupliceerde_lijnen[i + 1]}"
                gestructureerde_lijnen.append(samengevoegde_lijn)
                i += 2  # Sla de haakjes lijn over
            else:
                gestructureerde_lijnen.append(huidige_lijn)
                i += 1
        
        # STAP 4: Identificeer en formatteer de hoofddocumenttitel
        geformatteerde_lijnen = []
        hoofdtitel_gevonden = False
        
        for i, lijn in enumerate(gestructureerde_lijnen):
            # Sla veelvoorkomende metadata patronen over
            if (lijn.lower().startswith(('datum', 'versie', 'inhoud', 'pagina')) or
                ':' in lijn or
                lijn.startswith('#')):
                geformatteerde_lijnen.append(lijn)
                continue
            
            # Identificeer hoofdtitel: substantiële lijn vroeg in document, met hoofdletters
            if (not hoofdtitel_gevonden and 
                i < 15 and  # Binnen eerste 15 lijnen
                len(lijn) > 15 and  # Substantiële lengte
                not lijn.lower().startswith(('gelet', 'overwegende', 'artikel', 'besluit :')) and
                (lijn.isupper() or  # Alle hoofdletters
                 (len([woord for woord in lijn.split() if len(woord) > 2 and woord[0].isupper()]) >= 3))):  # Meerdere hoofdletterwoorden
                
                # Dit is de hoofdtitel
                geformatteerde_lijnen.append(f"# {lijn}")
                hoofdtitel_gevonden = True
            else:
                geformatteerde_lijnen.append(lijn)
        
        # STAP 5: Formatteer artikelnummers met vet
        finale_lijnen = []
        for lijn in geformatteerde_lijnen:
            # Formatteer artikelnummers: "Artikel" + nummer/romeins + optionele letter + punt
            
            # Patroon 1: Artikel 1, Artikel 2bis, etc.
            lijn = re.sub(r'^(Artikel\s+\d+(?:[a-z]+)?)\s*\.?\s*$', r'**\1.**', lijn)
            lijn = re.sub(r'^(Artikel\s+\d+(?:[a-z]+)?)\s*\.(\s)', r'**\1.**\2', lijn)
            
            # Patroon 2: Romeinse cijfers
            lijn = re.sub(r'^(Artikel\s+[IVXLCDM]+)\s*\.?\s*$', r'**\1.**', lijn)
            lijn = re.sub(r'^(Artikel\s+[IVXLCDM]+)\s*\.(\s)', r'**\1.**\2', lijn)
            
            # Patroon 3: Alleen "Artikel" aan begin van lijn (fallback)
            if lijn.strip().lower().startswith('artikel') and '**' not in lijn:
                lijn = re.sub(r'^(Artikel)', r'**\1**', lijn)
            
            finale_lijnen.append(lijn)
        
        # STAP 6: Voeg alles samen
        schone_tekst = '\n'.join(finale_lijnen)
        
        # STAP 7: Finale opschoning - zorg voor juiste spatiëring na punten in haakjes
        schone_tekst = re.sub(r'\(\s*([^)]+)\s*\)', r'( \1 )', schone_tekst)
        
        return {
            "succes": True,
            "document_id": document_id,
            "datum": datum,
            "url": url,
            "inhoud": schone_tekst,
            "html": response.text,
            "status_code": response.status_code
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "succes": False,
            "fout": str(e),
            "document_id": document_id,
            "datum": datum,
            "url": url
        } 