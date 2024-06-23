from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Noticias
from .forms import CrearNuevaNoticiaForm
from django.contrib.auth.models import User
import os

def noticias(request):
    noticias_list = Noticias.objects.order_by('-fecha_subida')[:3]
    return render(request, 'noticias.html', {'noticias': noticias_list})


def CrearNoticia(request):
    if request.method == 'POST':
        form = CrearNuevaNoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            # Procesar el campo de la imagen
            imagen = request.FILES['imagen']
            # Guardar la imagen en la carpeta de medios
            ruta_imagen = os.path.join(settings.MEDIA_ROOT, 'noticias', 'media', imagen.name)
            with open(ruta_imagen, 'wb') as archivo_destino:
                for parte in imagen.chunks():
                    archivo_destino.write(parte)

            # Crear una instancia del modelo Noticias
            noticia = Noticias(
                titulo=form.cleaned_data['titulo'],
                descripcion=form.cleaned_data['descripcion'],
                imagen=os.path.join('noticias', 'media', imagen.name),  # Guarda la ruta de la imagen en el modelo
                equipo=form.cleaned_data['equipo'],
                cuerpo=form.cleaned_data['cuerpo'],
                usuario=User.objects.get(username='JuanPablo')
            )
            noticia.save()  
            return redirect('/noticias')  
    else:
        form = CrearNuevaNoticiaForm()
    return render(request, 'crear_noticia.html', {'form': form})