import requests
from typing import Dict, Any

def vind_relatie(document_id: str) -> Dict[str, Any]:
    """
    Vind documentrelaties voor een specifiek document ID via de Vlaanderen API.
    
    Args:
        document_id (str): Het document ID om relaties voor te vinden
        
    Returns:
        Dict[str, Any]: De API response met documentrelaties
    """
    basis_url = "https://codex.opendata.api.vlaanderen.be:443/api/WetgevingDocument"
    url = f"{basis_url}/{document_id}/DocumentRelaties"
    
    try:
        # Maak de API request
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise een exception voor slechte status codes
        
        # Return de JSON response
        return {
            "succes": True,
            "data": response.json(),
            "status_code": response.status_code,
            "document_id": document_id
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "succes": False,
            "fout": str(e),
            "document_id": document_id
        } 