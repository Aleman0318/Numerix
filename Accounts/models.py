from django.contrib.auth.models import AbstractUser
from django.db import models

class UsuarioPersonalizado(AbstractUser):
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    carrera = models.CharField(max_length=100)
    carnet = models.CharField(max_length=20, unique=True)
    ciclo = models.CharField(max_length=20)

    def __str__(self):
        return self.username
