from urllib.request import urlopen
from bs4 import BeautifulSoup
from tkinter import messagebox
import tkinter
import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "exercise1.db")

conn = sqlite3.connect(db_path)
conn.close()

def almacenarProductos():
    page = urlopen('https://www.ulabox.com/en/campaign/productos-sin-gluten#gref')
    soup = BeautifulSoup(page, "html.parser")

    brands = []
    names = []
    links = []
    prices = []
    prices_without_discount = []
    ids = []


    all_products_list = soup.find_all('div', id = 'product-list')

    for product_list in all_products_list:
        all_articles = product_list.find_all('article')

        for article in all_articles:
            brands.append(article['data-product-brand'])
            names.append(article['data-product-name'])
            ids.append(article['data-product-id'])

            span = article.find('span', attrs = {'class':'product-grid-footer__price'})

            if(len(span.contents) == 1):
                strong = span.contents[0]
                prices_without_discount.append(0.0)
            else:
                del_ = span.contents[0]
                strong = span.contents[1]
                price_without_discount = del_.contents[0]
                prices_without_discount.append(float(price_without_discount[1:len(price_without_discount)]))
            
            price = float(strong.contents[0].contents[0] + '.' + strong.contents[1].contents[0][1:2])

            prices.append(price)
                
            
            a = article.find('a', class_ = 'product-item__image nauru js-pjax js-article-link')
            links.append(a['href'])

    conn = sqlite3.connect(db_path)

    conn.execute("DROP TABLE IF EXISTS PRODUCT")
    table = '''CREATE TABLE IF NOT EXISTS PRODUCT( \
        ID      INT     PRIMARY KEY     NOT NULL,\
        NAME    TEXT    NOT NULL,\
        BRAND   TEXT    NOT NULL,\
        LINK    TEXT    NOT NULL,\
        PRICE   FLOAT   NOT NULL,\
        PWOUTD  FLOAT   NOT NULL\
        );'''

    conn.execute(table)

    for i in range(len(brands)):
        conn.execute("""INSERT INTO PRODUCT VALUES (?,?,?,?,?,?)""", (ids[i], names[i], brands[i], links[i], prices[i],
        prices_without_discount[i]))

    conn.commit()
    conn.close()

    messagebox.showinfo("Info","Base de Datos Poblada con exito")

    tkinter.mainloop()

def mostrarMarca():
    b_part = tkinter.Tk()

    conn = sqlite3.connect(db_path)

    brands_list = conn.execute("""SELECT BRAND FROM PRODUCT""")
    brands_list = brands_list.fetchall()
    brands_list = list(dict.fromkeys(brands_list))

    j = []

    for i in brands_list:
        j.append(i[0])

    brands_list = j

    def search():
        result = w.get()

        result_list = conn.execute("SELECT NAME, PRICE FROM PRODUCT WHERE BRAND LIKE ?", (result,))
        result_list = list(dict.fromkeys(result_list))

        b_part_2 = tkinter.Tk()
        b_part_2.geometry("400x400")

        l = tkinter.Listbox(b_part_2, width=300, height=300)

        for i in range(len(result_list)):
            text = result_list[i][0] + ", " + str(result_list[i][1])
            l.insert(i, text)

        l.pack()

    w = tkinter.Spinbox(b_part, values = brands_list)
    b = tkinter.Button(b_part, text="Search", command=search)
    w.pack()
    b.pack()

    tkinter.mainloop()

def buscarOfertas():
    c_part = tkinter.Tk()
    c_part.geometry("400x400")

    conn = sqlite3.connect(db_path)

    l = tkinter.Listbox(c_part, width=300, height=300)

    result_list = conn.execute("SELECT NAME, PWOUTD, PRICE FROM PRODUCT WHERE PWOUTD NOT LIKE 0.0")
    result_list = list(dict.fromkeys(result_list))

    for i in range(len(result_list)):
        text = result_list[i][0] + ", " + str(result_list[i][1]) + ", " + str(result_list[i][2])
        l.insert(i, text)

    l.pack()

    tkinter.mainloop()

main = tkinter.Tk()
main.geometry("200x200")

b1 = tkinter.Button(main, text="Almacenar Productos", command = almacenarProductos)
b2 = tkinter.Button(main, text="Mostrar Marca", command = mostrarMarca)
b3 = tkinter.Button(main, text="Buscar Ofertas", command = buscarOfertas)

b1.pack()
b2.pack()
b3.pack()

tkinter.mainloop()