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
        messagebox.showinfo("Info","Base de Datos Poblada con exito")

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
            cursor = conn.execute("""SELECT NOMBRE, MARCA, PRECIO FROM ZAPATILLAS WHERE NOMBRE = ?""",(nombre,))
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
        cursor = conn.execute("SELECT NOMBRE, MARCA, PUNTUACION FROM ZAPATILLAS WHERE PUNTUACION != NONE AND NUMERO_PUNTUACION > 5 ORDER BY PUNTUACION DESC")
        result_list_2 = list(dict.fromkeys(cursor))

        l_2 = tkinter.Tk()
        l_2.geometry("400x400")

        list_2 = tkinter.Listbox(l_2, width=300, height=300)

        for i in range(len(result_list_2)):
                text = result_list_2[i][0] + ", " + result_list_2[i][1] + ", " + result_list_2[i][2]
                list_2.insert(i, text)

        list_2.pack()

        tkinter.mainloop()

    def marcas():
        m_1 = tkinter.Tk()
        m_1.geometry("200x200")

        elements = ['a', 'b', 'c']

        def buscarMarca():
            marca = m_spin.get()

            conn = sqlite3.connect('examen.db')
            conn.text_factory = str  
            cursor = conn.execute("""SELECT NOMBRE, MARCA, PRECIO, PUNTUACION FROM ZAPATILLAS WHERE MARCA = ?""", (marca,))
            result_list_3 = list(dict.fromkeys(cursor))

            l_3 = tkinter.Tk()
            l_3.geometry("400x400")

            list_3 = tkinter.Listbox(l_3, width=300, height=300)

            for i in range(len(result_list_3)):
                text = result_list_3[i][0] + ", " + result_list_3[i][1] + ", " + result_list_3[i][2] + ", " + result_list_3[i][3]
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