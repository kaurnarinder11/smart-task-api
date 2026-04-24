import requests
from typing import Dict, Any

def get_joke() -> Dict[str, Any]:
    """
    Fetch a random joke from the official joke API.
    
    Returns:
        Dict with either:
        - success=True, setup, punchline
        - success=False, error message
    """
    try:
        response = requests.get(
            "https://official-joke-api.appspot.com/random_joke",
            timeout=3
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "setup": data["setup"],
                "punchline": data["punchline"]
            }
        else:
            return {
                "success": False,
                "error": f"API returned status {response.status_code}"
            }
            
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Joke API is slow, try again later"
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Cannot connect to joke service"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }