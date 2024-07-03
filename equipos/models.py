from django.db import models

# Create your models here.

class Selecciones(models.Model):
    nombre = models.CharField(max_length=150)
    url = models.CharField(max_length=150, blank=True, null=True)

    
    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = 'Seleccion'
        verbose_name_plural = 'Selecciones'


class EquipoFutbol(models.Model):
    nombre = models.CharField(max_length=150)
    url = models.CharField(max_length=150, blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = 'Equipo Futbol'
        verbose_name_plural = 'Equipos de Futbol'