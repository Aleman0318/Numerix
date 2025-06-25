from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.MostrarHome, name='inicio'),
    path('creditos/', views.MostrarCreditos, name='ver_creditos')
]
