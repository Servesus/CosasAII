# Generated by Django 2.2.6 on 2020-01-21 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('idUser', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('nickname', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('idGame', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('tags', models.ManyToManyField(to='main.Tag')),
            ],
        ),
    ]
