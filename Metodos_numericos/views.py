from django.shortcuts import render
from .POO.lagrange import LagrangeSolver
from .POO.trazadores_cubicos import TrazadoresCubicosSolver
from django.utils import translation
from django.contrib.auth.decorators import login_required
from Historial.models import HistorialEjercicio


@login_required
def resolver_lagrange(request):
    translation.activate('es')

    if request.method == 'POST':
        data_x = request.POST.get('x')
        data_y = request.POST.get('y')

        try:
            # Convertir los datos
            valores_x = [float(val.strip()) for val in data_x.split(',')]
            valores_y = [float(val.strip()) for val in data_y.split(',')]

            # Validación
            if len(valores_x) != len(valores_y):
                raise ValueError("Los vectores X y Y deben tener la misma cantidad de elementos.")

            # Resolver el problema con Lagrange
            problema = LagrangeSolver(valores_x, valores_y)
            pasos_lagrange = problema.construir_polinomio()

            # Guardar en historial
            HistorialEjercicio.objects.create(
                usuario=request.user,
                metodo='Lagrange',
                pasos=pasos_lagrange,
                grafica_url=problema.grafica_url
            )

            # Renderizar resultado
            return render(request, 'resultado_lagrange.html', {
                'pasos': pasos_lagrange,
                'grafica_url': problema.grafica_url
            })

        except Exception as e:
            return render(request, 'formulario_lagrange.html', {
                'alerta_error': str(e)
            })

    return render(request, 'formulario_lagrange.html')


def resolver_trazadores(request):
    translation.activate('es')

    if request.method == 'POST':
        data_x = request.POST.get('x')
        data_y = request.POST.get('y')

        try:
            valores_x = [float(val.strip()) for val in data_x.split(',')]
            valores_y = [float(val.strip()) for val in data_y.split(',')]

            if len(valores_x) != len(valores_y):
                raise ValueError("Los vectores X y Y deben tener la misma cantidad de elementos.")

            # Resolver con trazadores cúbicos
            problema = TrazadoresCubicosSolver(valores_x, valores_y)
            pasos_trazadores = problema.resolver()
            grafica_url = problema.generar_grafica()

            # Guardar en historial
            HistorialEjercicio.objects.create(
                usuario=request.user,
                metodo='Trazadores Cúbicos',
                pasos=pasos_trazadores,
                grafica_url=grafica_url
            )

            return render(request, 'resultado_trazadores.html', {
                'pasos': pasos_trazadores,
                'grafica_url': grafica_url 
            })

        except Exception as e:
            return render(request, 'formulario_trazadores.html', {
                'alerta_error': str(e)
            })

    return render(request, 'formulario_trazadores.html')

@login_required
def showDocumentacion(request):
    return render(request, 'documentacion.html')

