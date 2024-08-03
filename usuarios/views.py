from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import CustomUser
from django.contrib.auth import get_user_model
from .forms import EditUserForm

User = get_user_model()


def user_permissions(request):
    if request.user.is_authenticated:
        return {
            'user_can_create_news': request.user.has_perm('noticias.add_noticia') or request.user.is_staff,
        }
    return {}

def signup(request):             # Registrar nuevo usuario

    if request.method == 'GET':
        return render(request, 'signup.html', {
        'form': UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # Register User
            try:
                user = CustomUser.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1'],
                email=request.POST['email'])
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
    return redirect('home')


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
        

from django.contrib.auth import update_session_auth_hash

def editar(request):
    user = request.user

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            if user.check_password(current_password):
                user = form.save(commit=False)
                if 'password' in form.cleaned_data and form.cleaned_data['password']:
                    user.set_password(form.cleaned_data['password'])
                    update_session_auth_hash(request, user)  # Actualiza la sesión para evitar cerrar la sesión
                user.save()
                return redirect('home')
            else:
                form.add_error('current_password', 'La contraseña actual es incorrecta.')
    else:
        form = EditUserForm(instance=user)

    return render(request, 'editar.html', {'form': form})