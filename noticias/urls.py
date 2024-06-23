from django.urls import path
from . import views

urlpatterns = [
    path('', views.noticias, name='home'),
    path('crear_noticia/', views.CrearNoticia, name='crear_noticia'),
]