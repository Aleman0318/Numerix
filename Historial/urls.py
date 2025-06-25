from django.urls import path
from . import views

urlpatterns = [
    path('historial/', views.ver_historial, name='ver_historial'),
]
