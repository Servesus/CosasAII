from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('eventos_fecha/',views.mostrar_eventos_fecha),
    path('eventos_frecuentes/',views.mostrar_tiposMasUsado),
    path('eventos_idioma/',views.mostrar_eventos_idioma),
    path('municipios_eventos/',views.mostrar_eventos),
    path('',views.index),
    path('index.html/', views.index),
    path('populate/', views.populateDatabase),
    path('ingresar/', views.ingresar),    
    path('admin/',admin.site.urls),
    ]
