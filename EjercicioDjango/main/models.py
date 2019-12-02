#encoding:utf-8

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Idioma(models.Model):
    idiomaId = models.TextField(primary_key=True)
    idioma = models.TextField(verbose_name= 'Idioma', help_text="Idioma")

    def __str__(self):
        return self.idioma
    
    class Meta:
        ordering = ('idioma', )

class Municipio(models.Model):
    municipioId = models.TextField(primary_key=True)
    municipio = models.TextField(verbose_name= 'Municipio', help_text="Municipio")

    def __str__(self):
        return self.municipio
    
    class Meta:
        ordering = ('municipio', )     

class TipoEvento(models.Model):
        
    tipo_evento = models.TextField(verbose_name='Tipo de Evento', help_text= "Tipo de evento")

    def __str__(self):
        return self.tipo_evento
    
    class Meta:
        ordering = ('tipo_evento', )      

class Evento(models.Model):
    eventoId = models.AutoField(primary_key=True)
    nombre = models.TextField(verbose_name='Evento', help_text= "Nombre del evento")
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio', help_text = "Fecha de inicio ")
    fecha_fin = models.DateField(verbose_name='Fecha de Finalización ', help_text = "Fecha de finalización")
    precio = models.DecimalField(verbose_name= 'Precio', help_text= "Precio", max_digits=5, decimal_places=2)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    tipo_evento = models.ForeignKey(TipoEvento, on_delete= models.CASCADE)
    idiomas = models.ManyToManyField(Idioma)
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('fecha_inicio', )

