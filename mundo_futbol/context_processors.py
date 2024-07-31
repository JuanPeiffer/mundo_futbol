# context_processors.py
from django.conf import settings

def football_api_key(request):
    return {'FOOTBALL_API_KEY': settings.FOOTBALL_API_KEY}
