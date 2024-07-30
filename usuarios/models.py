from django.contrib.auth.models import AbstractUser
from django.db import models
from equipos.models import EquipoFutbol

class CustomUser(AbstractUser):
    fecha_nacimiento = models.DateField(null=True, blank=True)
    equipo = models.ForeignKey(EquipoFutbol, on_delete=models.CASCADE, null=True, blank=True)
    twitter = models.CharField(max_length=35, null=True, blank=True)
    celular = models.CharField(max_length=15, null=True, blank=True)
    facebook = models.CharField(max_length=55, null=True, blank=True)
    instagram = models.CharField(max_length=35, null=True, blank=True)
    noticias_publicadas = models.IntegerField(default=0)

    def __str__(self):
        return self.username
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'