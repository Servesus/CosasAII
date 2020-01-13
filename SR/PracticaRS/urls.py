#encoding:utf-8

from django.urls import path
from django.contrib import admin
from main import views

urlpatterns = [
    path('', views.index),
    path('populate/', views.populateDB),
    path('loadRS', views.loadRS),
    #path('recommendedFilmsItems', views.recommendedFilmsItems),
    path('recommendedBooksUser', views.recommendedBooksUser),
    path('similarBooks', views.similarBooks),
    #path('recommendedUsersFilms', views.recommendedUsersFilms),
    path('search', views.search),
    path('admin/', admin.site.urls),
]