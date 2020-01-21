from bs4 import BeautifulSoup,NavigableString
from urllib.request import urlopen,Request
from tkinter import *
from tkinter import messagebox
import sqlite3
import re


"""
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
"""

def g2a(busqueda):
    nombres = []
    links = []
    precios = []
    imagenes = []
    site = "https://www.g2a.com/search?query="+busqueda
    hdr = {"authority": "www.g2a.com",
            "method": "GET",
            "path": "/search?query=gta",
            "scheme": "https",
            "accept-language": "es-ES,es;q=0.9,en;q=0.8",
            "referer": "https://www.g2a.com",
            "sec-fetch-mode": "navigate",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
    }
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page,"lxml")
    juegos = soup.find("ul",class_="products-grid")
    for juego in juegos:
        card_media = juego.find("div",class_="Card__media")
        link = "https://www.g2a.com" + card_media.a.get("href")
        try:
            imagen = card_media.a.find("img",class_="lazy-image__img Card__picture__img").get("data-src")
        except:
            imagen = ""
        nombre = juego.find("h3",class_="Card__title").a.string
        tags_precio = juego.find("div",class_="Card__body").find("div",class_="Card__footer").find("div",class_="Card__price").find("span",class_="Card__price-cost price")
        precio = str(tags_precio).split(">")[1].split("<")[0]
        nombres.append(nombre)
        links.append(link)
        precios.append(precio)
        imagenes.append(imagenes)
        return nombres,links,precios,imagenes
        

g2a("gta")