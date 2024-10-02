from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include


# SI NO TIENE NADA EN PATH '' ES XQ NO TIENE NADA ANTES DEL / EN LA URL
# POR EJEMPLO PATH '', INCLUDE 'equipos.urls' (SERIA LOCALHOST/BOCA) Y NO LOCALHOST/EQUIPOS/BOCA/
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('equipos.urls')),
    path('noticias/', include('noticias.urls')),
    path('', include('usuarios.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('equipos.urls')),
]

# Agregar las URL de los medios para la aplicación usuarios
# urlpatterns += static(settings.USUARIOS_MEDIA_URL, document_root=settings.USUARIOS_MEDIA_ROOT)

# Agregar las URL de los medios para la aplicación noticias
urlpatterns += static(settings.NOTICIAS_MEDIA_URL, document_root=settings.NOTICIAS_MEDIA_ROOT)