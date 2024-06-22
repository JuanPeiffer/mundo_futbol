from django.db import models

# Create your models here.
class EquipoFutbol(models.Model):
    nombre = models.CharField(max_length=150)
    url = models.CharField(max_length=150)
    
    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = 'Equipo Futbol'
        verbose_name_plural = 'Equipos de Futbol'

class Noticias(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=150)
    imagen = models.CharField(max_length=150)
    equipo = models.ForeignKey(EquipoFutbol, on_delete=models.CASCADE)
    cuerpo = models.TextField()
    fecha_subida = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['-fecha_subida']
        indexes = [
            models.Index(fields=['-fecha_subida']),
        ]
