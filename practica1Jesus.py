from bs4 import BeautifulSoup
import urllib.request as urllib2

url = "https://foros.derecho.com/foro/20-Derecho-Civil-General"

response = urllib2.urlopen(url)
webContent = response.read().decode("latin-1")
soup = BeautifulSoup(webContent, 'html.parser')
lista = soup.find(id="threads")
lista2 = lista.find_all("li")
titulos = []
enlaces = []
autores = []

for item in lista2:
    h3 = item.find_all("h3")
    for item2 in h3:
        if len(item2)>0:
            a = item2.find("a")
            titulo = a.string
            titulos.append(titulo)
            enlace_tema = "https://foros.derecho.com/" + a.get('href')
            enlaces.append(enlace_tema)
    autores2 = item.find_all(class_="author")
    for i in autores2:
        autor = i.find("a").string
        
    