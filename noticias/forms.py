from django import forms
from .models import Noticias
from ckeditor.widgets import CKEditorWidget

class CrearNuevaNoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticias
        fields = ['titulo', 'descripcion', 'imagen', 'equipo', 'cuerpo']
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'imagen': 'Imagen',
            'equipo': 'Equipo',
            'cuerpo': 'Cuerpo'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'data-browse': 'Elegir archivo'}),
            'equipo': forms.Select(attrs={'class': 'form-control'}),
            'cuerpo': CKEditorWidget(),
        }
