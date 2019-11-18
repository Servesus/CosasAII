encoding = "utf-8"
import urllib.request as urllib2
import datetime
import os.path
import os

from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in
from whoosh.index import open_dir


def llamadaObtencionDatos():
    
    i=1
    lista=[]
    
    while i<4:
        url="http://www.sensacine.com/noticias/?page="+str(i)
        if i == 1:
            lista=obtenerDatos(url)
        else:
            lista[0].extend(obtenerDatos(url)[0])
            lista[1].extend(obtenerDatos(url)[1])
            lista[2].extend(obtenerDatos(url)[2])
            lista[3].extend(obtenerDatos(url)[3])
            lista[4].extend(obtenerDatos(url)[4])
        i=i+1

    file = open('categorias.txt', "w")
    for i in range(len(lista[0])):
        file.write(lista[0][i] + os.linesep)
    file.close()

    file = open("titulos.txt", "w")
    for i in range(len(lista[1])):
        file.write(lista[1][i] + os.linesep)
    file.close()

    file = open("enlaces.txt", "w")
    for i in range(len(lista[2])):
        file.write(lista[2][i] + os.linesep)
    file.close()

    file = open("fechas.txt", "w")
    for i in range(len(lista[3])):
        file.write(str(lista[3][i]) + os.linesep)
    file.close()

    file = open("descripciones.txt", "w")
    for i in range(len(lista[4])):
        file.write(str(lista[4][i]) + os.linesep)
    file.close()

def obtenerDatos(url):
    
    urlBasica="http://www.sensacine.com/"
    response = urllib2.urlopen(url)
    webContent = response.read()
    soup = BeautifulSoup(webContent, 'html.parser')
    
    listaCategoria=[]
    listaTitulos=[]
    listaEnlaces=[]
    listaFechas=[]
    listaDescripciones=[]
    meses={"enero":"01", "febrero":"02", "marzo":"03", "abril":"04", "mayo":"05", "junio":"06", "julio":"07", "agosto":"08", "septiembre":"09", "octubre":"10", "noviembre":"11", "diciembre":"12" }
    
    for categorias in soup.findAll("div",attrs={"class":"meta-category"}):
        listaCategoria.append(categorias.string.split("-")[1].strip(" "))
    for titulos in soup.findAll("a",attrs={"class":"meta-title-link"}):
        listaTitulos.append(titulos.string.strip())
        listaEnlaces.append(urlBasica+titulos.get("href"))
    for fechas in soup.findAll("div",attrs={"class":"meta-date"}):
        fechaSinCasting=fechas.string.split(" ")[1]+ "/" + meses[fechas.string.split(" ")[3]] + "/" + fechas.string.split(" ")[5]
        fechasCasting= datetime.datetime.strptime(fechaSinCasting, '%d/%m/%Y')
        listaFechas.append(fechasCasting)
    for descripciones in soup.findAll("div",attrs={"class":"meta-body"}):
        listaDescripciones.append(descripciones.string)
        
    return listaCategoria, listaTitulos, listaEnlaces, listaFechas ,listaDescripciones

def cargar():
    
    categorias = Schema(name=ID(stored=True), content=TEXT)
    titulos = Schema(name=ID(stored=True), content=KEYWORD)
    enlaces = Schema(name=ID(stored=True), content=TEXT)
    fechas = Schema(name=ID(stored=True), content=DATETIME)
    descripciones = Schema(name=ID(stored=True), content=KEYWORD)

    schemas = [categorias, titulos, enlaces, fechas, descripciones]
    paths = []

    ix = index.create_in("indexdir3", schema)
    writer = ix.writer()
    path = "myRoko.txt"

    with open(path, "r") as f:
    content = f.read()
    f.close()
    writer.add_document(name=path, content= content)

    writer.commit()

    if not os.path.exists("index"):
        os.mkdir("index")

    ix = create_in("index", schema)
    ix = open_dir("index")

    writer = ix.writer()

    for i in range(len(lista[0])):
        writer.add_document(category=lista[0][i], title=lista[1][i], link=lista[2][i], 
            date=lista[3][i], description=lista[4][i])
    
    writer.commit()

    searcher = ix.searcher()

    #with ix.searcher() as searcher: