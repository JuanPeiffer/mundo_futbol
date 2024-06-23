from django import forms
from .models import EquipoFutbol

class CrearNuevaNoticiaForm(forms.Form):
    titulo = forms.CharField(
        max_length=100, 
        label='Titulo',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    descripcion = forms.CharField(
        max_length=100, 
        label='Descripcion',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    imagen = forms.ImageField(
    label='Imagen',
    widget=forms.ClearableFileInput(attrs={'class': 'form-control-file', 'data-browse': 'Elegir archivo'})
)

    equipo = forms.ModelChoiceField(
        queryset=EquipoFutbol.objects.all(), 
        label='Equipo',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cuerpo = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Cuerpo'
    )
