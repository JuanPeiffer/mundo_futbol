from django.http import HttpResponse
from django.shortcuts import render
from .models import Noticias

def index(request):
    return render(request, 'noticias.html')
    
def noticias(request):
    noticias = Noticias.objects.all()
    return render(request, 'noticias.html', {'noticias': noticias})