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

    def contenidoTitulo():
        n_1 = tkinter.Tk()
        n_1.geometry("200x200")

        def buscarContenidoTitulo():
            #contenido = n_entry.get()

            contenido = "algo Y poco NO esto"

            contenido = contenido.replace('Y', 'and')
            contenido = contenido.replace('O', 'or')
            contenido = contenido.replace('NO', 'not')

            #result_list_1 = list(dict.fromkeys(cursor))

            l_1 = tkinter.Tk()
            l_1.geometry("400x400")

            list_1 = tkinter.Listbox(l_1, width=300, height=300)

            list_1.pack()
        
        n_entry = tkinter.Entry(n_1)
        n_button = tkinter.Button(n_1, text="Buscar", command = buscarContenidoTitulo)

        n_entry.pack()
        n_button.pack()

        tkinter.mainloop()


    def fecha():
        n_1 = tkinter.Tk()
        n_1.geometry("200x200")

        def buscarFecha():
            #nombre = n_entry.get()

            nombre = "23/10/2005 Tarde"

            elements = nombre.split()

            #result_list_1 = list(dict.fromkeys(cursor))

            l_1 = tkinter.Tk()
            l_1.geometry("400x400")

            list_1 = tkinter.Listbox(l_1, width=300, height=300)

            list_1.pack()
        
        n_entry = tkinter.Entry(n_1)
        n_button = tkinter.Button(n_1, text="Buscar", command = buscarFecha)

        n_entry.pack()
        n_button.pack()

        tkinter.mainloop()

    def fechaTitulo():
        n_1 = tkinter.Tk()
        n_1.geometry("200x200")

        def buscarFechaTitulo():
            #fecha = n_entry.get()
            #titulo = n_entry_2.get()

            fecha = "20091023"
            titulo = "hola"

            #result_list_1 = list(dict.fromkeys(cursor))

            l_1 = tkinter.Tk()
            l_1.geometry("400x400")

            list_1 = tkinter.Listbox(l_1, width=300, height=300)

            list_1.pack()
        
        n_entry = tkinter.Entry(n_1)
        n_entry_2 = tkinter.Entry(n_1)
        n_button = tkinter.Button(n_1, text="Buscar", command = buscarFechaTitulo)

        n_entry.pack()
        n_entry_2.pack()
        n_button.pack()

        tkinter.mainloop()


    b_part_b1 = tkinter.Button(b_part, text="Contenido y titulo", command = contenidoTitulo)
    b_part_b2 = tkinter.Button(b_part, text="Fecha", command = fecha)
    b_part_b3 = tkinter.Button(b_part, text="Titulo y fecha", command = fechaTitulo)

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

#aa

tkinter.mainloop()