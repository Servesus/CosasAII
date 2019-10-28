from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3

def extraer():
    nombres = []
    marcas = []
    precios = []
    precios_oferta = []
    puntuaciones = []
    numero_puntuaciones = []
    for i in range(1,4):
        f = urllib.request.urlopen("https://www.sprinter.es/zapatillas-de-hombre?page="+str(i)+"&per_page=20")
        s = BeautifulSoup(f,"lxml")
        productos = s.find_all("div",class_="product__data")
        for producto in productos:
            nombre = producto.a.string
            nombres.append(nombre)
            marcas.append(producto.a.string.split(" ")[0])
            try:
                precio_old = producto.find("span",class_="product__price--old").contents[0]
            except:
                precio_old = None
            precio_actual = producto.find("span",class_="product__price--actual").string
            if precio_old == None:
                precios.append(precio_actual)
                precios_oferta.append(None)    
            else:
                precios.append(precio_old)
                precios_oferta.append(precio_actual)            
            
            url_nueva = "https://www.sprinter.es" + producto.a.get("href")
            f2 = urllib.request.urlopen(url_nueva)
            s2 = BeautifulSoup(f2,"lxml")
            div_dots = div_dots = s2.find("div",class_="average")
            rating = div_dots.span.string
            total = s2.find("div",class_="stats").find("meta",attrs = {'itemprop':'reviewCount'})
            puntuaciones_total = total['content']
            puntuaciones.append(rating)
            numero_puntuaciones.append(puntuaciones_total)
            print(rating)

    return nombres,marcas,precios,precios_oferta,puntuaciones,numero_puntuaciones
            
        

extraer()


