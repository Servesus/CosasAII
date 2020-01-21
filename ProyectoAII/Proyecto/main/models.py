from django.db import models
from django.core.validators import URLValidator

class User(models.Model):
    idUser = models.CharField(max_length=100, primary_key=True)
    nickname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Tag(models.Model):
    name = models.CharField(max_length=100)

class Game(models.Model):
    idGame = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=300)
    tags = models.ManyToManyField(Tag)