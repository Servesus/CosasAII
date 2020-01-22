#encoding:utf-8

from django.urls import path
from django.contrib import admin
from main import views

urlpatterns = [
    path('', views.index),
    path('populate/', views.populateDB),
    path('loadRS/', views.loadRS),
    path('searchSimilar', views.specific),
    path('search', views.search),
    path('recommend/<str:idGame>', views.CBRecommendationSystem),
    path('admin/', admin.site.urls),
]