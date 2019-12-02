from django.test import TestCase
from main.models import Evento, Idioma, TipoEvento, Municipio
from main.forms import EventosFechaForm, EventosIdiomaForm
from datetime import datetime
import csv

# Create your tests here.
def populate():
    #drops
    Municipios.objects.all().delete()
    TipoEvento.objects.all().delete()
    Idioma.objects.all().delete()
    Evento.objects.all().delete()
    #populates
    populateMunicipios()
    populateTipoEvento()
    populateIdioma()
    with open('dataset-B.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for i in range(1, len(csv_reader)):
            Evento.objects.create(eventoId = i-1, nombre = csv_reader[i][0],
            tipo_evento = TipoEvento.objects.get(tipo_evento = csv_reader[i][1],
            fecha_inicio = datetime.strptime(csv_reader[i][2], '%d/%m/%Y')),
            fecha_fin = datetime.strptime(csv_reader[i][3], '%d/%m/%Y')),
            precio = float(csv_reader[i][4]),
            idioma = Idioma.objects.get(idioma = csv_reader[i][5]),
            municipio = Municipio.objects.get(municipio = csv_reader[i][6]))

def populateMunicipios():
    with open('municipio.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        for i in range(1, len(csv_reader)):
            Municipio.objects.create(municipioId = i-1, municipio = csv_reader[i])

def populateTipoEvento():
    with open('tipoevento.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        for i in range(1, len(csv_reader)):
            TipoEvento.objects.create(tipoEventoId = i-1, tipo_evento = csv_reader[i])

def populateIdioma():
    with open('lenguas.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        for i in range(1, len(csv_reader)):
            Idioma.objects.create(idiomaId = i-1, idioma = csv_reader[i])


populate():
