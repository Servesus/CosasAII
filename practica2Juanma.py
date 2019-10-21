from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3
import practica2Jesus as lists

def almacenar_bd():
    conn = sqlite3.connect('practica2.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS PRODUCTOS") 
    conn.execute('''CREATE TABLE PRODUCTOS
       (MARCA           TEXT NOT NULL,
       NOMBRE           TEXT    NOT NULL,
       LINK             TEXT    NOT NULL,
       PRECIO_ORIGINAL  TEXT    NOT NULL,
       PRECIO_OFERTA    TEXT );''')

    todas_las_marcas, todos_los_nombres,todas_las_url,todos_los_precios, todos_los_precios_oferta = lists.funcion()
    for i, value in enumerate(todas_las_marcas):
        conn.execute("""INSERT INTO PRODUCTOS VALUES (?,?,?,?,?)""",(todas_las_marcas[i], todos_los_nombres[i], todas_las_url[i],
        todos_los_precios[i], todos_los_precios_oferta[i]))
    
    conn.commit()

    cursor = conn.execute("SELECT marca, nombre, link, precio_original, precio_oferta from PRODUCTOS")
    for row in cursor:
        print("MARCA = ", row[0])
        print("NOMBRE = ", row[1])
        print("LINK = ", row[2])
        print("PRECIO_ORIGINAL = ", row[3])
        print("PRECIO_OFERTA = ", row[4], "\n")
    conn.close()

almacenar_bd()
