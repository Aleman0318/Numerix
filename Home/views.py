from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.

# vista para Home
def MostrarHome(request):
    return render(request, 'home/index.html')

@login_required
def MostrarCreditos(request):
    return render(request, 'home/creditos.html')