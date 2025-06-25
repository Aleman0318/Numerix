from django.shortcuts import render
from .POO.lagrange import LagrangeSolver
from .POO.trazadores_cubicos import TrazadoresCubicosSolver
from sympy import latex  

def resolver_lagrange_prueba(request):
    if request.method == 'POST':
        x_data = request.POST.get('x')
        y_data = request.POST.get('y')

        try:
            x_vals = [float(val.strip()) for val in x_data.split(',')]
            y_vals = [float(val.strip()) for val in y_data.split(',')]

            if len(x_vals) != len(y_vals):
                raise ValueError("Los vectores X y Y deben tener la misma cantidad de elementos.")

            solver = LagrangeSolver(x_vals, y_vals)
            solver.construir_polinomio()

            
            resultado_latex = latex(solver.polinomio_expandido)

            return render(request, 'resultado_lagrange_prueba.html', {
                'x_vals': x_vals,
                'y_vals': y_vals,
                'resultado': resultado_latex
            })

        except Exception as e:
            return render(request, 'formulario_lagrange_prueba.html', {'alerta_error': str(e)})

    return render(request, 'formulario_lagrange_prueba.html')


def resolver_trazadores_prueba(request):
    if request.method == 'POST':
        x_data = request.POST.get('x')
        y_data = request.POST.get('y')

        try:
            x_vals = [float(val.strip()) for val in x_data.split(',')]
            y_vals = [float(val.strip()) for val in y_data.split(',')]

            if len(x_vals) != len(y_vals):
                raise ValueError("Los vectores X y Y deben tener la misma cantidad de elementos.")

            solver = TrazadoresCubicosSolver(x_vals, y_vals)
            resultado = solver.resolver()

            return render(request, 'resultado_trazadores_prueba.html', {
                'x_vals': x_vals,
                'y_vals': y_vals,
                'resultado': resultado[-1]['contenido']  
            })

        except Exception as e:
            return render(request, 'formulario_trazadores_prueba.html', {'alerta_error': str(e)})

    return render(request, 'formulario_trazadores_prueba.html')


def mostrarCreditosPrueba(request):
    return render(request, 'creditos_prueba.html')

def mostrarDocumentacionPrueba(request):
    return render(request, 'documentacion_prueba.html')