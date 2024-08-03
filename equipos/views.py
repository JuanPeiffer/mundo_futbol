from django.http import HttpResponse
from django.shortcuts import render,redirect

def index(request):
    return render(request, 'index.html')

def about(request):
    return HttpResponse("Sobre mundo")

