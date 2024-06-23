from django.http import HttpResponse
from django.shortcuts import render
from .models import Noticias

def noticias(request):
    noticias_list = Noticias.objects.order_by('-fecha_subida')[:3]
    return render(request, 'noticias.html', {'noticias': noticias_list})
