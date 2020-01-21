#encoding:utf-8

from django.urls import path
from django.contrib import admin
from main import views

urlpatterns = [
    path('', views.index),
    path('populate/', views.populateDB),
    #path('loadRS', views.loadRS),
    #path('similarGames', views.similarGames),
    path('search', views.search),
    path('offers/<str:idGame>', views.offers),
    path('admin/', admin.site.urls),
]