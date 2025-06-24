from typing import List, Dict, Any

def krijg_beschikbare_tools() -> List[Dict[str, Any]]:
    """
    Geef een lijst van beschikbare tools voor de agent terug.
    
    Returns:
        List[Dict[str, Any]]: Lijst van tool definities
    """
    return [
        {
            "name": "zoek_vlaamse_codex_api",
            "description": "Zoek in de Vlaanderen wetgeving API naar documenten die specifieke termen bevatten",
            "parameters": {
                "type": "object",
                "properties": {
                    "zoekterm": {
                        "type": "string",
                        "description": "De term om te zoeken in de wetgeving API, gebruikt enkel integrale zinnen om te zoeken in de API"
                    }
                },
                "required": ["zoekterm"]
            }
        },
        {
            "name": "vind_relatie",
            "description": "Vind documentrelaties voor een specifiek document ID om te ontdekken welk origineel document het wijzigt",
            "parameters": {
                "type": "object",
                "properties": {
                    "document_id": {
                        "type": "string",
                        "description": "Het document ID om relaties voor te vinden"
                    }
                },
                "required": ["document_id"]
            }
        },
        {
            "name": "krijg_voorlaatste_versie",
            "description": "Krijg de HTML inhoud van het originele document van Vlaanderen Codex. Gebruik dit ALLEEN NADAT je het originele document ID hebt gevonden door je analyse.",
            "parameters": {
                "type": "object",
                "properties": {
                    "document_id": {
                        "type": "string",
                        "description": "Het originele document ID om op te halen"
                    },
                    "datum": {
                        "type": "string",
                        "description": "De datum om een specifieke versie van het document op te halen (YYYY-MM-DD formaat). Gebruik een datum die VOOR de meest recente wijziging ligt om de voorlaatste (tweede meest recente) versie te krijgen, niet de allerlaatste of allereerste versie."
                    }
                },
                "required": ["document_id"]
            }
        }
    ] 