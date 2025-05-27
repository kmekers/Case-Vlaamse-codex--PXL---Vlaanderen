import requests
import urllib.parse
from typing import Dict, Any

def zoek_vlaamse_codex_api(zoekterm: str) -> Dict[str, Any]:
    """
    Zoek in de Vlaanderen wetgevingsdatabase naar documenten.
    
    Args:
        zoekterm (str): De term om te zoeken in de wetgevingsdatabase
        
    Returns:
        Dict[str, Any]: De API response met zoekresultaten
    """
    basis_url = "https://codex.opendata.api.vlaanderen.be:443/api/WetgevingDocument/Zoeken"
    
    # URL encode de zoekterm
    gecodeerde_zoekterm = urllib.parse.quote(zoekterm)
    
    # Construeer de volledige URL
    url = f"{basis_url}?zoekTerm={gecodeerde_zoekterm}"
    
    try:
        # Maak de API request
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise een exception voor slechte status codes
        
        # Return de JSON response
        return {
            "succes": True,
            "data": response.json(),
            "status_code": response.status_code,
            "zoekterm": zoekterm
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "succes": False,
            "fout": str(e),
            "zoekterm": zoekterm
        } 