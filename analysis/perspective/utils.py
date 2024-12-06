# analysis/utils.py
import requests
from django.conf import settings

def analyze_text(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "languages": ["es"],  # Cambia esto si necesitas soporte para otros idiomas
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    params = {"key": settings.PERSPECTIVE_API_KEY}
    
    response = requests.post(url, headers=headers, json=data, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to analyze text", "details": response.json()}
