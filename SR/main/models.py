from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,URLValidator
    
class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    idioma = models.CharField(max_length=100)
    genero = models.CharField(max_length=100)
    rating1 = models.PositiveIntegerField()
    rating2 = models.PositiveIntegerField()
    rating3 = models.PositiveIntegerField()
    rating4 = models.PositiveIntegerField()
    rating5 = models.PositiveIntegerField()
    def __str__(self):
        return self.titulo

    
class Puntuacion(models.Model):
    userId = models.PositiveIntegerField()
    Libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    def __str__(self):
        return str(self.rating)