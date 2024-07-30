import requests
from django.conf import settings

def get_football_data(endpoint):
    url = f"https://api-football-v1.p.rapidapi.com/v3/{endpoint}"
    headers = {
        'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com',
        'X-RapidAPI-Key': settings.FOOTBALL_API_KEY
    }
    response = requests.get(url, headers=headers)
    return response.json()
