from django.test import TestCase
import csv

# Create your tests here.
def populate():
    with open('dataset-B.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for i in range(1, len(csv_reader)):
            Evento.objects.create(nombre = )


populate():
