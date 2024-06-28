from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

def signup(request):             # Registrar nuevo usuario

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
def signout(request):            #  Cerrar la sesión
    logout(request)
    return redirect('login')

def signin(request):             # Iniciar sesión
    if request.method == 'GET':
        return render(request, 'login.html', {
        'form': AuthenticationForm
    })
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {
            'form': AuthenticationForm,
            'error': "Usuario o contraseña incorrectos"
            })
        
def logout(request): # Cerrar la sesión
    logout(request)
    return redirect('login')
