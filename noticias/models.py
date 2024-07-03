from django.db import models
from equipos.models import EquipoFutbol, Selecciones
from ckeditor.fields import RichTextField
from django.conf import settings



class Noticias(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    imagen = models.ImageField()
    equipo = models.ForeignKey(EquipoFutbol, on_delete=models.CASCADE, blank=True, null=True)
    seleccion = models.ForeignKey(Selecciones, on_delete=models.CASCADE, blank=True, null=True)
    cuerpo = RichTextField()
    fecha_subida = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['-fecha_subida']
        indexes = [
            models.Index(fields=['-fecha_subida']),
        ]