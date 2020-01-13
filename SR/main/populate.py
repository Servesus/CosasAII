from main.models import Libro,Puntuacion
from datetime import datetime
import csv

path = "ml-100k"

def deleteTables():  
    Libro.objects.all().delete()
    Puntuacion.objects.all().delete()
    
    
def populateDatabase():
    deleteTables()
    populateLibro()
    populatePuntuacion()

if __name__ == '__main__':
    populateLibro()

def populateLibro():
    lista = []
    with open(path+'\\bookfeatures.csv',encoding="latin-1") as csv_file:
        csv_reader = list(csv.reader(csv_file, delimiter=';'))
        for i in range(1,len(csv_reader)):
            if len(csv_reader[i]) == 10 :
                lista.append(Libro(id=csv_reader[i][0],titulo=csv_reader[i][1],autor=csv_reader[i][2],
                genero=csv_reader[i][3],idioma=csv_reader[i][4],rating1=csv_reader[i][5],
                rating2=csv_reader[i][6],rating3=csv_reader[i][7],rating4=csv_reader[i][8],rating5=csv_reader[i][9]))
            else:
                lista.append(Libro(id=csv_reader[i][0],titulo=csv_reader[i][1]+csv_reader[i][2],autor=csv_reader[i][3],
                genero=csv_reader[i][4],idioma=csv_reader[i][5],rating1=csv_reader[i][6],
                rating2=csv_reader[i][7],rating3=csv_reader[i][8],rating4=csv_reader[i][9],rating5=csv_reader[i][10]))
        Libro.objects.bulk_create(lista)

def populatePuntuacion():
    lista = []
    with open(path+'\\ratings.csv',encoding="latin-1") as csv_file:
        csv_reader = list(csv.reader(csv_file, delimiter=';'))
        for i in range(1,len(csv_reader)):
            lista.append(Puntuacion(rating=csv_reader[i][0],libro = Libro.objects.get(id=csv_reader[i][2]),
            userId = csv_reader[i][1]))
        Puntuacion.objects.bulk_create(lista)