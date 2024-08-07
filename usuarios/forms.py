from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email', 'fecha_nacimiento']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class EditUserForm(forms.ModelForm):
    current_password = forms.CharField(label='Contraseña actual', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    profile_image = forms.ImageField(required=False, label='Imagen de perfil')

    class Meta:
        model = CustomUser
        fields = ['username', 'equipo', 'first_name', 'last_name', 'fecha_nacimiento', 'email', 'celular', 'instagram',
                  'twitter', 'facebook', 'profile_image']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'equipo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@email.com'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario de Instagram'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario de Twitter'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link de Facebook'}),
        }
