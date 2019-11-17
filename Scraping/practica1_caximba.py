from tkinter import *

top = Tk()

def datos():
    top2 = Tk()

    def cargar():
        top3 = Tk()

        top3.mainloop()

    def mostrar():
        top4 = Tk()

        top4.mainloop()

    def salir():
        top2.destroy()
    
    d1 = Button(top2, text = "Cargar", command = cargar)
    d1.place(x = 40, y = 5)

    d2 = Button(top2, text = "Mostrar", command = mostrar)
    d2.place(x = 40, y = 35)

    d3 = Button(top2, text = "Salir", command = salir)
    d3.place(x = 40, y = 65)


    top2.mainloop()

def buscar():
    top2 = Tk()

    def tema():
        top3 = Tk()

        top3.mainloop()

    def fecha():
        top4 = Tk()

        top4.mainloop()
    
    d1 = Button(top2, text = "Tema", command = tema)
    d1.place(x = 40, y = 5)

    d2 = Button(top2, text = "Fecha", command = fecha)
    d2.place(x = 40, y = 35)

    top2.mainloop()

def estadisticas():
    top2 = Tk()

    def temasMasPopulares():
        top3 = Tk()

        top3.mainloop()

    def temasMasActivos():
        top4 = Tk()

        top4.mainloop()
    
    d1 = Button(top2, text = "Temas mas populares", command = temasMasPopulares)
    d1.place(x = 40, y = 5)

    d2 = Button(top2, text = "Temas mas activos", command = temasMasActivos)
    d2.place(x = 40, y = 35)

    top2.mainloop()


B = Button(top, text = "Datos", command = datos)
B.place(x = 40, y = 5)

B2 = Button(top, text = "Buscar", command = buscar)
B2.place(x = 40, y = 35)

B3 = Button(top, text = "Estadisticas", command = estadisticas)
B3.place(x = 40, y = 65)

top.mainloop()