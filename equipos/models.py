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
    nombre = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    historia = models.TextField(blank=True, null=True)
    fecha_fundacion = models.DateField(blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = 'Equipo Futbol'
        verbose_name_plural = 'Equipos de Futbol'