from django.conf import settings

def football_api_key(request):
    return {'FOOTBALL_API_KEY': settings.FOOTBALL_API_KEY}

from django.utils.functional import SimpleLazyObject

# en mundo_futbol/context_processors.py
def user_permissions(request):
    if request.user.is_authenticated:
        return {
            'user_can_create_news': request.user.has_perm('noticias.add_noticia') or request.user.is_staff,
        }
    return {}


def user_permissions_processor(request):
    return user_permissions(request)