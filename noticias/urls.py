from django.urls import path
from . import views

urlpatterns = [
    path('', views.noticias, name='home'),
    path('crear_noticia/', views.CrearNoticia, name='crear_noticia'),
    path('<int:noticia_id>/', views.ver_noticia, name='ver_noticia'),
    path('<int:noticia_id>/editar/', views.editar_noticia, name='editar_noticia'),
    path('<int:noticia_id>/borrar/', views.borrar_noticia, name='borrar_noticia'),
]