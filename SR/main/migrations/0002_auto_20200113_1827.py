# Generated by Django 2.2.5 on 2020-01-13 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='puntuacion',
            old_name='Libro',
            new_name='libro',
        ),
    ]
