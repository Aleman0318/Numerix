from django.urls import path
from . import views

urlpatterns = [
    path('lagrange/', views.resolver_lagrange_prueba, name='lagrange_prueba'),
    path('trazadores/', views.resolver_trazadores_prueba, name='trazadores_prueba'),
    path('creditos/', views.mostrarCreditosPrueba, name='creditos_prueba'),
    path('documentacion/', views.mostrarDocumentacionPrueba, name='documentacion_prueba')
]
