from urllib.request import urlopen
from bs4 import BeautifulSoup
from tkinter import messagebox
import tkinter
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

def datos():
    a_part = tkinter.Tk()
    a_part.geometry("200x200")

    def cargar():

        dirdocs = r"C:\Users\ercax\Desktop\Cosas python\CosasAII\Whoosh\txts"

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
            #print("Se han almacenado "+ str(len(titulos))+" noticias")
            messagebox.showinfo( "Base Datos", "Se han almacenado "+ str(len(titulos))+" noticias")
            tkinter.mainloop()
            

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

        whooshFunction(dirdocs)

    def salir():
        a_part.destroy()
    

    a_part_b1 = tkinter.Button(a_part, text="Cargar", command = cargar)
    a_part_b2 = tkinter.Button(a_part, text="Salir", command = salir)

    a_part_b1.pack()
    a_part_b2.pack()

    tkinter.mainloop()

def buscar():
    b_part = tkinter.Tk()
    b_part.geometry("200x200")

    def contenidoTitulo():
        n_1 = tkinter.Tk()
        n_1.geometry("200x200")

        def buscarContenidoTitulo():
            #contenido = n_entry.get()

            contenido = "algo Y poco NO esto"

            palabras = contenido.split()

            for i in range(len(palabras)):
                if palabras[i] == 'Y':
                    palabras[i] = palabras[i].replace('Y', 'and')
                elif palabras[i] == 'O':
                    palabras[i] = palabras[i].replace('O', 'or')
                elif palabras[i] == 'NO':
                    palabras[i] = palabras[i].replace('NO', 'not')

            #result_list_1 = list(dict.fromkeys(cursor))

            l_1 = tkinter.Tk()
            l_1.geometry("400x400")

            list_1 = tkinter.Listbox(l_1, width=300, height=300)

            list_1.pack()
        
        n_entry = tkinter.Entry(n_1)
        n_button = tkinter.Button(n_1, text="Buscar", command = buscarContenidoTitulo)

        n_entry.pack()
        n_button.pack()

        tkinter.mainloop()


    def fecha():
        n_1 = tkinter.Tk()
        n_1.geometry("200x200")

        def buscarFecha():
            #nombre = n_entry.get()

            nombre = "23/10/2005 Tarde"

            elements = nombre.split()

            #result_list_1 = list(dict.fromkeys(cursor))

            l_1 = tkinter.Tk()
            l_1.geometry("400x400")

            list_1 = tkinter.Listbox(l_1, width=300, height=300)

            list_1.pack()
        
        n_entry = tkinter.Entry(n_1)
        n_button = tkinter.Button(n_1, text="Buscar", command = buscarFecha)

        n_entry.pack()
        n_button.pack()

        tkinter.mainloop()

    def fechaTitulo():
        n_1 = tkinter.Tk()
        n_1.geometry("200x200")

        def buscarFechaTitulo():
            #fecha = n_entry.get()
            #titulo = n_entry_2.get()

            fecha = "20091023"
            titulo = "hola"

            #result_list_1 = list(dict.fromkeys(cursor))

            l_1 = tkinter.Tk()
            l_1.geometry("400x400")

            list_1 = tkinter.Listbox(l_1, width=300, height=300)

            list_1.pack()
        
        n_entry = tkinter.Entry(n_1)
        n_entry_2 = tkinter.Entry(n_1)
        n_button = tkinter.Button(n_1, text="Buscar", command = buscarFechaTitulo)

        n_entry.pack()
        n_entry_2.pack()
        n_button.pack()

        tkinter.mainloop()


    b_part_b1 = tkinter.Button(b_part, text="Contenido y titulo", command = contenidoTitulo)
    b_part_b2 = tkinter.Button(b_part, text="Fecha", command = fecha)
    b_part_b3 = tkinter.Button(b_part, text="Titulo y fecha", command = fechaTitulo)

    b_part_b1.pack()
    b_part_b2.pack()
    b_part_b3.pack()

    tkinter.mainloop()


main = tkinter.Tk()
main.geometry("200x200")

b1 = tkinter.Button(main, text="Datos", command = datos)
b2 = tkinter.Button(main, text="Buscar", command = buscar)

b1.pack()
b2.pack()

#aa

tkinter.mainloop()