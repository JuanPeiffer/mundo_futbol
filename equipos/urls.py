from django.urls import path
from . import views
from .views import equipo_detalle

urlpatterns = [
    path('', views.index, name='home'),
    path('equipo/<int:equipo_id>/', equipo_detalle, name='equipo_detalle'),
]