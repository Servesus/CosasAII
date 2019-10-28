from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3

def almacenar_bd():
    conn = sqlite3.connect('examen.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS ") 
    conn.execute('''CREATE TABLE ZAPATILLAS
       (NOMBRE              TEXT    NOT NULL,
        MARCA               TEXT    NOT NULL,
        PRECIO              TEXT    NOT NULL,
        PRECIO_OFERTA       TEXT            ,
        PUNTUACION          INTEGER         ,
        NUMERO_PUNTUACION   INTEGER);''')

    todas_las_marcas, todos_los_nombres,todas_las_url,todos_los_precios, todos_los_precios_oferta = lists.funcion()
    for i, value in enumerate(todas_las_marcas):
        conn.execute("""INSERT INTO PRODUCTOS VALUES (?,?,?,?,?,?)""",(todas_las_marcas[i], todos_los_nombres[i], todas_las_url[i],
        todos_los_precios[i], todos_los_precios_oferta[i]))
    
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM ZAPATILLAS")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " zapatillas")
    conn.close()

def buscar_nombre_bd(nombre):
    conn = sqlite3.connect('examen.db')
    conn.text_factory = str  
    cursor = conn.execute("""SELECT NOMBRE, MARCA, PRECIO FROM ZAPATILLAS WHERE NOMBRE = ?""",(nombre,))
    print(cursor)
    conn.close()

def ordenar_puntuacion_bd():
    conn = sqlite3.connect('examen.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT NOMBRE, MARCA, PUNTUACION FROM ZAPATILLAS WHERE PUNTUACION != NONE ORDER BY PUNTUACION DESC")
    print(cursor)
    conn.close()

def buscar_marca_bd(marca):
    conn = sqlite3.connect('examen.db')
    conn.text_factory = str  
    cursor = conn.execute("""SELECT NOMBRE, MARCA, PRECIO, PUNTUACION FROM ZAPATILLAS WHERE MARCA = ?""", (marca,))
    print(cursor)
    conn.close()