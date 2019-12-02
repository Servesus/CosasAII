from urllib.request import urlopen
from bs4 import BeautifulSoup
from tkinter import messagebox

import tkinter
import sqlite3
import os.path
import practica2WhooshManuel as shit

main = tkinter.Tk()
main.geometry("200x200")

b1 = tkinter.Button(main, text="Datos", command = shit.llamadaObtencionDatos())
#b2 = tkinter.Button(main, text="Buscar", command = buscar)

b1.pack()
#b2.pack()

tkinter.mainloop()