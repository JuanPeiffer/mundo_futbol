from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Noticias
from .forms import CrearNuevaNoticiaForm
from django.contrib.auth.models import User
import os
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

def noticias(request):   # Cards de noticias
    noticias_list = Noticias.objects.order_by('-fecha_subida')[:3]
    return render(request, 'noticias.html', {'noticias': noticias_list})

@login_required
def CrearNoticia(request):  # Crear nueva noticia
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
                # usuario=User.objects.get(username='JuanPablo')
                usuario=User.objects.get(username=request.user.username)
            )
            noticia.save()  
            return redirect('/noticias')  
    else:
        form = CrearNuevaNoticiaForm()
    return render(request, 'crear_noticia.html', {'form': form})

@login_required
def editar_noticia(request, noticia_id):    # Editar noticia
    noticia = get_object_or_404(Noticias, pk=noticia_id)

    if request.method == 'POST':
        form_edit = CrearNuevaNoticiaForm(request.POST, request.FILES, instance=noticia)
        if form_edit.is_valid():
            # Eliminar la imagen anterior si hay una nueva imagen proporcionada
            if 'imagen' in request.FILES:
                # Obtener la ruta de la imagen anterior y eliminarla del sistema de archivos
                if noticia.imagen:
                    ruta_imagen_anterior = os.path.join(settings.MEDIA_ROOT, noticia.imagen.name)
                    if os.path.exists(ruta_imagen_anterior):
                        os.remove(ruta_imagen_anterior)
                
                # Procesar y guardar la nueva imagen
                imagen_nueva = request.FILES['imagen']
                ruta_imagen_nueva = os.path.join(settings.MEDIA_ROOT, 'noticias', 'media', imagen_nueva.name)
                with open(ruta_imagen_nueva, 'wb') as archivo_destino:
                    for parte in imagen_nueva.chunks():
                        archivo_destino.write(parte)

                # Actualizar la instancia de Noticias con la nueva imagen
                noticia.imagen = os.path.join('noticias', 'media', imagen_nueva.name)

            # Guardar otros campos de la noticia
            noticia.titulo = form_edit.cleaned_data['titulo']
            noticia.descripcion = form_edit.cleaned_data['descripcion']
            noticia.equipo = form_edit.cleaned_data['equipo']
            noticia.cuerpo = form_edit.cleaned_data['cuerpo']
            noticia.usuario = request.user
            noticia.save()

            return redirect('/noticias')
    else:
        form_edit = CrearNuevaNoticiaForm(instance=noticia)

    return render(request, 'editar_noticia.html', {'noticia': noticia, 'form': form_edit})

def ver_noticia(request, noticia_id): # Ver Noticia
    noticia = get_object_or_404(Noticias, pk=noticia_id)
    return render(request, 'ver_noticia.html', {'noticia' : noticia})

# ---------------------------------------------------------------- #

@login_required
def borrar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticias, pk=noticia_id)
    if request.method == 'POST':
        noticia.delete()
        return redirect('/noticias')
    return render(request, 'borrar_noticia.html', {'noticia' : noticia})
