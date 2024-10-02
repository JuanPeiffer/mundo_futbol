from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from .models import EquipoFutbol

def index(request):
    return render(request, 'index.html')

def about(request):
    return HttpResponse("Sobre mundo")

def equipo_detalle(request, equipo_id):
    equipo = get_object_or_404(EquipoFutbol, id=equipo_id)
    return render(request, 'equipos/equipo_detalle.html', {'equipo': equipo})
