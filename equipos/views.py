from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError


# Create your views here.
def index(request):
    return render(request, 'index.html')
def about(request):
    return HttpResponse("Sobre mundo")

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
        'form': UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # Register User
            try:
                user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': "Ya existe un usuario con ese nombre"
                }) 
            
        return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': "Las cotraseñas no coinciden"
                })