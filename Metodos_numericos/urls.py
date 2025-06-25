from django.urls import path
from . import views

urlpatterns = [
    path('lagrange/', views.resolver_lagrange, name='formulario_lagrange'),
    path('trazadores/', views.resolver_trazadores, name='formulario_trazadores'),
    path('documentacion/', views.showDocumentacion, name='documentacion_metodos'),
]
