from django.contrib.auth.models import AbstractUser
from django.db import models
from equipos.models import EquipoFutbol

class CustomUser(AbstractUser):
    fecha_nacimiento = models.DateField(null=True, blank=True)
    equipo = models.ForeignKey(EquipoFutbol, on_delete=models.CASCADE, null=True, blank=True)
    twitter = models.TextField(null=True, blank=True)
    celular = models.TextField(null=True, blank=True)
    facebook = models.TextField(null=True, blank=True)
    instagram = models.TextField(null=True, blank=True)
    whatsapp = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'