from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Historial.models import HistorialEjercicio

@login_required
def ver_historial(request):
    historial = HistorialEjercicio.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'historial.html', {
        'historial': historial
    })
