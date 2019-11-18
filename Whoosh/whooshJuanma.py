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

def extraer():
    titulos = []
    fechas = []
    enlaces = []
    textos = []
    url = "https://www.sevilla.org/actualidad/noticias?b_start:int=0"
    url2 = "https://www.sevilla.org/actualidad/noticias?b_start:int=9"
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response.read().decode("utf-8"), 'lxml')

    noticias = soup.find_all("div",class_="tile col-xs-12 col-sm-6 col-lg-4 mb-4")
    for noticia in noticias:
        enlace = noticia.find("a").get("href")
        enlaces.append(enlace)
        response2 = urllib.request.urlopen(enlace)
        soup2 = BeautifulSoup(response2.read().decode("utf-8"), 'lxml')
        titulo = soup2.find("h1",class_="documentFirstHeading text-secondary mt-0 mb-5").string
        titulos.append(titulo)
        texto = soup2.find("p",class_="documentDescription description mb-4 text-semi h4-size mt-0").string
        textos.append(texto)
        fecha = noticia.find("p",class_="small text-gray mt-3 mb-2").string
        fechas.append(fecha)
    
    response3 = urllib.request.urlopen(url2)
    soup3 = BeautifulSoup(response3.read().decode("utf-8"), 'lxml')

    noticias2 = soup3.find_all("div",class_="tile col-xs-12 col-sm-6 col-lg-4 mb-4")
    for noticia in noticias2:
        enlace = noticia.find("a").get("href")
        enlaces.append(enlace)
        response2 = urllib.request.urlopen(enlace)
        soup2 = BeautifulSoup(response2.read().decode("utf-8"), 'lxml')
        titulo = soup2.find("h1",class_="documentFirstHeading text-secondary mt-0 mb-5").string
        titulos.append(titulo)
        texto = soup2.find("p",class_="documentDescription description mb-4 text-semi h4-size mt-0").string
        textos.append(texto)
        fecha = noticia.find("p",class_="small text-gray mt-3 mb-2").string
        fechas.append(fecha)
        
    return titulos,fechas,enlaces,textos

def crearTxt(dirdocs):
    titulos,fechas,enlaces,textos = extraer()
    if not os.path.isdir(dirdocs):
        os.mkdir(dirdocs)
    for i in range(0,len(titulos)):
        file_object = open(dirdocs + "/Archivo"+str(i)+".txt","w")
        file_object.write(str(titulos[i]))
        file_object.write("\n")
        file_object.write(str(fechas[i]))
        file_object.write("\n")
        file_object.write(str(enlaces[i]))
        file_object.write("\n")
        file_object.write(str(textos[i]))
    print("Se han almacenado "+ str(len(titulos))+" noticias")


def whooshFunction(dirdocs):
    crearTxt(dirdocs)
    schema = Schema(titulo=TEXT(stored=True), fecha=fields.DATETIME(stored=True), enlace=TEXT(stored=True), resumen=TEXT(stored=True))

    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

    ix = index.create_in("indexdir", schema)
    writer = ix.writer()
    for docname in os.listdir(dirdocs):
        if not os.path.isdir(dirdocs+docname):
            fileobj=open(dirdocs+'\\'+docname, "r")
            tit=fileobj.readline().strip()
            f=fileobj.readline().strip()
            fech=datetime.strptime(f,'%d/%m/%Y - %H:%M')
            enl=fileobj.readline().strip()
            res=fileobj.readline().strip()
            fileobj.close()           
            
            writer.add_document(titulo = tit, fecha = fech, enlace = enl, resumen = res)
    writer.commit()

def buscador_a(texto):
    ix = index.open_dir("indexdir")
    myquery = '{'+ texto + 'TO 20200101 000000]' 
    with ix.searcher() as searcher:
        query = QueryParser("fecha", ix.schema).parse(myquery)
        results = searcher.search(query)
        for r in results:
            print(r['titulo'])

