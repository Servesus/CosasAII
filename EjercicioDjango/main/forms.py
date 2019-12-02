#encoding:utf-8
from django import forms
   
class EventosFechaForm(forms.Form):
    fecha = forms.DateField(label="Fecha del evento", widget=forms.TextInput, required=True)
    
class PeliculaBusquedaYearForm(forms.Form):
    idioma = forms.CharField(label="Idioma del evento", widget=forms.TextInput, required=True)