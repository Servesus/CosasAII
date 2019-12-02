from bs4 import BeautifulSoup
import urllib.request
import datetime


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



