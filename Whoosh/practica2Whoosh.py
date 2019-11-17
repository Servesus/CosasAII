from bs4 import BeautifulSoup
import urllib.request
import datetime
from tkinter import *
from tkinter import messagebox
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
import os, os.path
from whoosh import index,fields
from datetime import datetime
from whoosh.qparser import QueryParser




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
    response = urllib.request.urlopen(url)
    
    soup = BeautifulSoup(response.read().decode("utf-8"), 'lxml')
    
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
            fechasCasting= datetime.strptime(fechaSinCasting, '%d/%m/%Y')
            listaFechas.append(fechasCasting)
        for descripciones in soup.findAll("div",attrs={"class":"meta-body"}):
            listaDescripciones.append(descripciones.string)
        
    return listaCategoria, listaTitulos, listaEnlaces, listaFechas ,listaDescripciones

def crearTxt(dirdocs):
    lista = llamadaObtencionDatos()
    if not os.path.isdir(dirdocs):
        os.mkdir(dirdocs)
    for i in range(0,len(lista[0])):
        file_object = open(dirdocs + "/Archivo"+str(i)+".txt","w")
        file_object.write(str(lista[0][i]))
        file_object.write("\n")
        file_object.write(str(lista[1][i]))
        file_object.write("\n")
        file_object.write(str(lista[2][i]))
        file_object.write("\n")
        file_object.write(str(lista[3][i]))
        file_object.write("\n")
        a = lista[4][i]
        b = str(a)
        file_object.write(b)

def whooshFunction(dirdocs):
    crearTxt(dirdocs)
    schema = Schema(categoria=TEXT(stored=True),
                titulo=TEXT(stored=True),
                enlace=ID(stored=True),
                descripcion=TEXT(analyzer=StemmingAnalyzer()),
                fecha=fields.DATETIME(stored=True))

    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

    ix = index.create_in("indexdir", schema)
    writer = ix.writer()
    for docname in os.listdir(dirdocs):
        if not os.path.isdir(dirdocs+docname):
            fileobj=open(dirdocs+'\\'+docname, "r")
            cat=fileobj.readline().strip()
            tit=fileobj.readline().strip()
            enlc=fileobj.readline().strip()
            f=fileobj.readline().strip()
            fech=datetime.strptime(f,'%Y-%m-%d %H:%M:%S')
            descrp=fileobj.readline().strip()
            fileobj.close()           
            
            writer.add_document(categoria = cat, titulo = tit, enlace = enlc, descripcion = descrp, fecha = fech)
    writer.commit()

def buscador(texto):
    ix = index.open_dir("indexdir")
    myquery = '{'+ texto + 'TO 20200101 000000]' 
    with ix.searcher() as searcher:
        query = QueryParser("fecha", ix.schema).parse(myquery)
        results = searcher.search(query)
        for r in results:
            print(r['titulo'])

dirdocs = "D:/Documentos/Universidad/4º/CosasAII/Archivitos"
#whooshFunction(dirdocs)
buscador("20180101 000000")
