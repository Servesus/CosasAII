#encoding:utf-8
from main.models import Evento, Idioma, TipoEvento, Municipio
from main.forms import EventosFechaForm, EventosIdiomaForm
from django.shortcuts import render
from django.db.models import Avg
from django.http.response import HttpResponseRedirect, HttpResponse
from django.conf import settings
from datetime import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

import csv

path = "data"

def populateDatabase(request):
    #drops
    Municipio.objects.all().delete()
    TipoEvento.objects.all().delete()
    Idioma.objects.all().delete()
    Evento.objects.all().delete()
    #populates
    populateMunicipios()
    populateTipoEvento()
    populateIdioma()
    with open(path+'\\dataset-B.csv') as csv_file:
        csv_reader = list(csv.reader(csv_file, delimiter=';'))
        
        for i in range(1,len(csv_reader)):
            print(csv_reader[i][1])
            Evento.objects.create(eventoId = i-1, nombre = csv_reader[i][0],
            idioma = Idioma.objects.get(idioma = csv_reader[i][5]),
            tipo_evento = TipoEvento.objects.get(tipo_evento = csv_reader[i][1]),
            fecha_inicio = datetime.strptime(csv_reader[i][2], '%d/%m/%Y'),
            fecha_fin = datetime.strptime(csv_reader[i][3], '%d/%m/%Y'),
            precio = float(csv_reader[i][4]),
            municipio = Municipio.objects.get(municipio = csv_reader[i][6]))

def populateMunicipios():
    with open(path+'\\municipio.csv') as csv_file:
        csv_reader = list(csv.reader(csv_file))
        row_count = sum(1 for row in csv_reader)
        for i in range(1, row_count):
            Municipio.objects.create(municipioId = i-1, municipio = csv_reader[i])
def populateTipoEvento():
    with open(path+'\\tipoevento.csv') as csv_file:
        csv_reader = list(csv.reader(csv_file))
        for i in range(1, len(csv_reader)):
            TipoEvento.objects.create(tipo_evento = csv_reader[i])
    print("2")

def populateIdioma():
    with open(path+'\\lenguas.csv') as csv_file:
        csv_reader = list(csv.reader(csv_file))
        for i in range(1, len(csv_reader)):
            Idioma.objects.create(idiomaId = i-1, idioma = csv_reader[i])
    print("3")

def mostrar_eventos(request):
    eventos = Evento.objects.all().order_by("municipio")
    return render(request, "municipios_eventos.html",{"eventos":eventos, 'STATIC_URL':settings.STATIC_URL})

def mostrar_tiposMasUsado(request):
    tipoEventos = TipoEvento.objects.all()
    tipo1, tipo2 = None, None
    for i in range(len(tipoEventos)):
        if tipo1 == None:
            tipo1 == [tipoEventos[i][0],tipoEventos[i][1]]
        elif tipo2 == None:
            tipo2 == [tipoEventos[i][0],tipoEventos[i][1]]
        else:
            count = Evento.objects.all().filter(tipoEvento = tipoEvento[i][1]).count()
            if count >= tipo1[0]:
                tipo1 = [tipoEventos[i][0],tipoEventos[i][1]]
            elif count >= tipo2[0]:
                tipo2 = [tipoEventos[i][0],tipoEventos[i][1]]

    result = [tipo1[1],tipo2[1]]
    
    return render(request, "eventos_frecuentes.html",{"eventos":result, 'STATIC_URL':settings.STATIC_URL})

def mostrar_eventos_fecha(request):
    formulario = EventosFechaForm()
    eventos = None
    
    if request.method=='POST':
        formulario = EventosFechaForm(request.POST)
        
        if formulario.is_valid():
            eventos = Evento.objects.filter(fecha_inicio=formulario.cleaned_data['fecha'])
            
    return render(request, 'eventos_fecha.html', {'formulario':formulario, 'eventos':eventos, 'STATIC_URL':settings.STATIC_URL})

def mostrar_eventos_idioma(request):
    formulario = EventosIdiomaForm()
    eventos = None
    
    if request.method=='POST':
        formulario = EventosFechaForm(request.POST)
        
        if formulario.is_valid():
            eventos = Evento.objects.filter(idioma=formulario.cleaned_data['idioma'])
            
    return render(request, 'eventos_idioma.html', {'formulario':formulario, 'eventos':eventos, 'STATIC_URL':settings.STATIC_URL})
        
def index(request):
    return render(request, 'index.html',{'STATIC_URL':settings.STATIC_URL})