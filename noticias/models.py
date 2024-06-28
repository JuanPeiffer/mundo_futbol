from django.db import models
from equipos.models import EquipoFutbol
from ckeditor.fields import RichTextField


class Noticias(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    imagen = models.ImageField()
    equipo = models.ForeignKey(EquipoFutbol, on_delete=models.CASCADE)
    cuerpo = RichTextField()
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