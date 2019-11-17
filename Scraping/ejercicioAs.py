from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3

def extraer():
    f = urllib.request.urlopen("http://resultados.as.com/resultados/futbol/primera/2018_2019/calendario/")
    s = BeautifulSoup(f,"lxml")
    jornadas = s.find_all("div",class_="cont-modulo resultados")
    equipos_lo = []
    equipos_vis = []
    goles_lo = []
    goles_vis = []
    links = []

    for jornada in jornadas:
        partidos = jornada.find_all("tr",id=True)
        for partido in partidos:
            equipos = partido.find_all("span", class_="nombre-equipo")
            local = equipos[0].string
            equipos_lo.append(local)
            visitante = equipos[1].string
            equipos_vis.append(visitante)
            resultado = partido.find("a", class_="resultado")
            goles = resultado.string.split("-")
            goles_local = goles[0]
            goles_lo.append(goles_local)
            goles_visitante = goles[1]
            goles_vis.append(goles_visitante)
            link = resultado.get("href")
            links.append(link)
    
    return equipos_lo,equipos_vis,goles_lo,goles_vis,links

