encoding = "utf-8"
from bs4 import BeautifulSoup
import urllib.request as urllib2
import datetime
from tkinter import *
from tkinter import messagebox


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
     
    return lista

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
        