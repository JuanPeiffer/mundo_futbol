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
    nombre = models.CharField(max_length=255)
    logo = models.URLField()
    ciudad = models.TextField(blank=True)
    historia = models.TextField(blank=True)
    apodo = models.CharField(max_length=100, blank=True)
    director_tecnico = models.CharField(max_length=255, blank=True)
    presidente = models.CharField(max_length=255, blank=True)
    vicepresidente = models.CharField(max_length=255, blank=True)
    cantidad_socios = models.IntegerField(null=True, blank=True)
    goleador_historico = models.CharField(max_length=255, blank=True)
    jugadores_historicos = models.JSONField(blank=True, null=True)  # Almacena una lista de jugadores históricos
    jugador_mas_partidos = models.CharField(max_length=255, blank=True)
    jugador_mas_titulos = models.CharField(max_length=255, blank=True)
    entrenador_mas_ganador = models.CharField(max_length=255, blank=True)
    estadio = models.CharField(max_length=255, blank=True)
    plantel_actual = models.JSONField(blank=True, null=True)  # Almacena una lista de jugadores actuales
    
    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = 'Equipo Futbol'
        verbose_name_plural = 'Equipos de Futbol'