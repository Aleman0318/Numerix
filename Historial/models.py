# Historial/models.py
from django.db import models
from django.conf import settings

class HistorialEjercicio(models.Model):
    METODOS = [
        ('Lagrange', 'Interpolación de Lagrange'),
        ('Trazadores Cúbicos', 'Trazadores Cúbicos Naturales'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    metodo = models.CharField(max_length=50, choices=METODOS)
    fecha = models.DateTimeField(auto_now_add=True)
    pasos = models.JSONField()  # Almacenamos lista de pasos tipo {"tipo": ..., "contenido": ...}
    grafica_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.usuario} - {self.metodo} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
