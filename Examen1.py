from urllib.request import urlopen
from bs4 import BeautifulSoup
from tkinter import messagebox
import tkinter
import sqlite3
import os.path

def datos():
    a_part = tkinter.Tk()
    a_part.geometry("200x200")

    def cargar():

        nombres = []
        marcas = []
        precios = []
        precios_oferta = []
        puntuaciones = []
        numero_puntuaciones = []

        for i in range(1,4):
            f = urlopen("https://www.sprinter.es/zapatillas-de-hombre?page="+str(i)+"&per_page=20")
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
                f2 = urlopen(url_nueva)
                s2 = BeautifulSoup(f2,"lxml")
                div_dots = div_dots = s2.find("div",class_="average")
                rating = div_dots.span.string
                total = s2.find("div",class_="stats").find("meta",attrs = {'itemprop':'reviewCount'})
                puntuaciones_total = total['content']
                puntuaciones.append(rating)
                numero_puntuaciones.append(puntuaciones_total)

        conn = sqlite3.connect('examen.db')
        conn.text_factory = str
        conn.execute("DROP TABLE IF EXISTS ZAPATILLAS") 
        conn.execute('''CREATE TABLE ZAPATILLAS
        (NOMBRE              TEXT    NOT NULL,
            MARCA               TEXT    NOT NULL,
            PRECIO              TEXT    NOT NULL,
            PRECIO_OFERTA       TEXT            ,
            PUNTUACION          INTEGER         ,
            NUMERO_PUNTUACION   INTEGER);''')

        for i, values in enumerate(marcas):
            conn.execute("""INSERT INTO ZAPATILLAS VALUES (?,?,?,?,?,?)""",(nombres[i], marcas[i], precios[i],
            precios_oferta[i], int(puntuaciones[i]), int(numero_puntuaciones[i])))
        
        conn.commit()
        cursor = conn.execute("SELECT COUNT(*) FROM ZAPATILLAS")
        messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " zapatillas")
        conn.close()

        tkinter.mainloop()

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

    def nombre():
        n_1 = tkinter.Tk()
        n_1.geometry("200x200")

        def buscarNombre():
            nombre = n_entry.get()

            conn = sqlite3.connect('examen.db')
            conn.text_factory = str  
            #cursor = conn.execute("""SELECT NOMBRE, MARCA, PRECIO FROM ZAPATILLAS WHERE NOMBRE LIKE ?""",(nombre,))
            cursor = conn.execute("SELECT NOMBRE, MARCA, PRECIO FROM ZAPATILLAS WHERE NOMBRE LIKE '%" + nombre + "%'")
            result_list_1 = list(dict.fromkeys(cursor))

            l_1 = tkinter.Tk()
            l_1.geometry("400x400")

            list_1 = tkinter.Listbox(l_1, width=300, height=300)

            for i in range(len(result_list_1)):
                text = result_list_1[i][0] + ", " + result_list_1[i][1] + ", " + result_list_1[i][2]
                list_1.insert(i, text)

            list_1.pack()
        
        n_entry = tkinter.Entry(n_1)
        n_button = tkinter.Button(n_1, text="Buscar", command = buscarNombre)

        n_entry.pack()
        n_button.pack()

        tkinter.mainloop()


    def ordenarPorPuntuacion():
        conn = sqlite3.connect('examen.db')
        conn.text_factory = str  
        cursor = conn.execute("SELECT NOMBRE, MARCA, PUNTUACION FROM ZAPATILLAS WHERE NUMERO_PUNTUACION > 5 ORDER BY PUNTUACION DESC")
        result_list_2 = list(dict.fromkeys(cursor))

        l_2 = tkinter.Tk()
        l_2.geometry("400x400")

        list_2 = tkinter.Listbox(l_2, width=300, height=300)

        for i in range(len(result_list_2)):
                text = result_list_2[i][0] + ", " + result_list_2[i][1] + ", " + str(result_list_2[i][2])
                list_2.insert(i, text)

        list_2.pack()

        tkinter.mainloop()

    def marcas():
        m_1 = tkinter.Tk()
        m_1.geometry("200x200")

        conn = sqlite3.connect('examen.db')

        brands_list = conn.execute("""SELECT MARCA FROM ZAPATILLAS""")
        brands_list = brands_list.fetchall()
        brands_list = list(dict.fromkeys(brands_list))

        j = []

        for i in brands_list:
            j.append(i[0])

        elements = j

        def buscarMarca():
            marca = m_spin.get()

            conn.text_factory = str  
            cursor = conn.execute("""SELECT NOMBRE, MARCA, PRECIO, PUNTUACION FROM ZAPATILLAS WHERE MARCA = ?""", (marca,))
            result_list_3 = list(dict.fromkeys(cursor))

            l_3 = tkinter.Tk()
            l_3.geometry("400x400")

            list_3 = tkinter.Listbox(l_3, width=300, height=300)

            for i in range(len(result_list_3)):
                text = result_list_3[i][0] + ", " + result_list_3[i][1] + ", " + result_list_3[i][2] + ", " + str(result_list_3[i][3])
                list_3.insert(i, text)

            list_3.pack()
        
        m_spin = tkinter.Spinbox(m_1, values = elements)
        m_button = tkinter.Button(m_1, text="Buscar", command = buscarMarca)

        m_spin.pack()
        m_button.pack()

        tkinter.mainloop()


    b_part_b1 = tkinter.Button(b_part, text="Nombre", command = nombre)
    b_part_b2 = tkinter.Button(b_part, text="Ordenar por puntuacion", command = ordenarPorPuntuacion)
    b_part_b3 = tkinter.Button(b_part, text="Marcas", command = marcas)

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

tkinter.mainloop()