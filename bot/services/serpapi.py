import requests
from config.settings import SERPAPI_KEY

def perform_web_search(query):
    params = {
        "q": query,
        "api_key": SERPAPI_KEY
    }
    response = requests.get("https://serpapi.com/search", params=params).json()
    return response.get("organic_results", [])