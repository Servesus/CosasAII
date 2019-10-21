from bs4 import BeautifulSoup
import urllib.request as urllib2

url = "https://www.ulabox.com/campaign/productos-sin-gluten#gref"
url2 = "https://www.ulabox.com/"

response = urllib2.urlopen(url)
webContent = response.read().decode("utf-8")
soup = BeautifulSoup(webContent, 'html.parser')

todas_listas_productos = soup.find_all(id="product-list")

todas_las_marcas = []
todos_los_nombres = []
todas_las_url = []
todos_los_precios = []
todos_los_precios_oferta =[] 

for listas_productos in todas_listas_productos:
    productos = listas_productos.find_all(class_="islet")
    for producto in productos:
        marcas = producto.find_all("h4")
        nombres = producto.find_all("h3")
        for marca in marcas:
            marca1 = marca.find("a").string.strip()
            todas_las_marcas.append(marca1)
        for h3 in nombres:
            url_producto = url2 + h3.find("a").get("href")
            nombre = h3.find("a").string.strip()
            todos_los_nombres.append(nombre)
            todas_las_url.append(url_producto)
    
    pies = listas_productos.find_all(class_="product-grid-footer__price")
    for pie in pies:
        precio = ""
        precio_anterior = None
        try:
            precio_anterior = pie.find("del").string
        except:
            precio_anterior = None
        for precio1 in pie.find("strong").find_all("span"):
            precio = precio + precio1.string
            if precio_anterior == None:
                todos_los_precios.append(precio)
                todos_los_precios_oferta.append(None)
            else:
                todos_los_precios.append(precio_anterior)
                todos_los_precios_oferta.append(precio)
            


