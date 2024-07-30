from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'fecha_nacimiento', 'equipo','noticias_publicadas', 'celular', 'twitter', 'facebook', 'instagram']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email', 'fecha_nacimiento', 'equipo','noticias_publicadas', 'twitter', 'celular', 'facebook', 'instagram')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    search_fields = ['username', 'email', 'equipo_nombre']
    ordering = ['username']

admin.site.register(CustomUser, CustomUserAdmin)
