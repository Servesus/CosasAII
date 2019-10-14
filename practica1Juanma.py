import sqlite3

conn = sqlite3.connect('Práctica 1/practica1.db')

print("Opened database successfully")

conn.execute('''CREATE TABLE PUBLICACION
         (ID INT PRIMARY KEY        NOT NULL,
         TITULO           TEXT      NOT NULL,
         TEMA             TEXT      NOT NULL,
         AUTOR            TEXT      NOT NULL,
         FECHA            DATETIME   NOT NULL,
         RESPUESTAS       INTEGER   NOT NULL,
         VISITAS          INTEGER   NOT NULL);''')

print ("Table created successfully")

conn.execute("INSERT INTO PUBLICACION(ID,TITULO,TEMA,AUTOR,FECHA, RESPUESTAS, VISITAS) \
      VALUES (1, 'Título', 'Derecho', 'Juanma Garrocho', '2013-10-07 08:23:19.120', 2, 2)")

conn.commit()
print ("Publications created successfully")

cursor = conn.execute("SELECT id, titulo, tema, autor, fecha, respuestas, visitas from PUBLICACION")
for row in cursor:
   print ("ID = " ,row[0])
   print ("TITULO = ", row[1])
   print ("TEMA = ", row[2])
   print ("AUTOR = ", row[3])
   print ("FECHA = ", row[4]) 
   print ("RESPUESTAS = ", row[5])
   print ("VISITAS = ", row[6] , "\n")

print ("Operation done successfully")

cursor2 = conn.execute("SELECT * from PUBLICACION WHERE autor == 'Juanma Garrocho'")
for row in cursor2:
   print ("ID = " ,row[0])
   print ("TITULO = ", row[1])
   print ("TEMA = ", row[2])
   print ("AUTOR = ", row[3])
   print ("FECHA = ", row[4]) 
   print ("RESPUESTAS = ", row[5])
   print ("VISITAS = ", row[6] , "\n")

print("Done")   
conn.close()



