from django.urls import path
from .views import LoginPersonalizado
from django.contrib.auth.views import LogoutView
from .views import registro_usuario;
from . import views

urlpatterns = [
    path('login/', LoginPersonalizado.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'), #enviara directo al login cuando hagamos logout
    path('registro/', registro_usuario, name='registro'),
    path('mi-perfil/', views.ver_perfil, name='ver_perfil' ),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),

]