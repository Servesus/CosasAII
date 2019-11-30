from django.db import models

# Create your models here.
class Ocupacion(models.Model):
    nombre = models.CharField()

class Usuario(models.Model):
    idUsuario = models.CharField(primary_key=True)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=1)
    codigoPostal = models.IntegerField()
    ocupacion = models.ForeignKey(Ocupacion, on_delete=models.PROTECT)

class Categoria(models.Model):
    idCategoria = models.CharField(primary_key=True)
    nombre = models.CharField()

class Pelicula(models.Model):
    idPelicula = models.CharField(primary_key=True)
    titulo = models.CharField()
    fechaEstreno = models.DateTimeField()
    categoria = models.ManyToManyField(Categoria)
    iMDbURL = models.CharField()

class Puntuacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(primary_key=True)
