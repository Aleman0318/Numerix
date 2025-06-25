import sympy as sym
import matplotlib.pyplot as plt
import numpy as np
import uuid
import os
from sympy import Symbol, latex, simplify
from django.apps import apps

class TrazadoresCubicosSolver:
    def __init__(self, x, y):
        self.x_valores = [float(val) for val in x]
        self.y_valores = [float(val) for val in y]
        self.n = len(x) - 1
        self.pasos = []
        self.grafica_url = None

    def redondear(self, valor):
        return round(float(valor), 4)

    def resolver(self):
        x = self.x_valores
        y = self.y_valores
        n = self.n
        x_sym = Symbol("x")

        self.pasos.append({"tipo": "texto", "contenido": "Los datos ingresados por el usuario fueron"})
        self.pasos.append({"tipo": "formula", "contenido": f"x = \\{{{', '.join(map(str, x))}\\}}"})
        self.pasos.append({"tipo": "formula", "contenido": f"y = \\{{{', '.join(map(str, y))}\\}}"})

        h = [x[i+1] - x[i] for i in range(n)]
        self.pasos.append({"tipo": "texto", "contenido": "Calculamos los intervalos hᵢ = xᵢ₊₁ - xᵢ"})
        for i in range(n):
            self.pasos.append({"tipo": "texto", "contenido": f"◈ Intervalo {i}"})
            self.pasos.append({"tipo": "formula", "contenido": f"h_{{{i}}} = x_{{{i+1}}} - x_{{{i}}}"})
            self.pasos.append({"tipo": "formula", "contenido": f"h_{{{i}}} = {x[i+1]} - {x[i]}"})
            self.pasos.append({"tipo": "formula", "contenido": f"h_{{{i}}} = {self.redondear(h[i])}"})

        A = sym.zeros(n - 1)
        b_vec = sym.zeros(n - 1, 1)
        self.pasos.append({"tipo": "texto", "contenido": "Luego construimos el sistema A · c = b"})
        for i in range(1, n):
            A[i-1, i-1] = 2 * (h[i-1] + h[i])
            if i > 1:
                A[i-1, i-2] = h[i-1]
            if i < n - 1:
                A[i-1, i] = h[i]
            b_expr = 3 * ((y[i+1] - y[i]) / h[i] - (y[i] - y[i-1]) / h[i-1])
            b_vec[i-1, 0] = b_expr
            self.pasos.append({"tipo": "formula", "contenido": f"b_{{{i-1}}} = {self.redondear(b_expr)}"})

        self.pasos.append({"tipo": "texto", "contenido": "La matriz A y vector b obtenidos son:"})
        self.pasos.append({"tipo": "formula", "contenido": f"A = {latex(A)}"})
        self.pasos.append({"tipo": "formula", "contenido": f"b = {latex(b_vec)}"})

        c_interior = A.LUsolve(b_vec)
        c = [0.0] + [round(c_interior[i, 0], 4) for i in range(n - 1)] + [0.0]
        self.pasos.append({"tipo": "texto", "contenido": "Resolvemos el sistema A · c = b"})
        self.pasos.append({"tipo": "formula", "contenido": f"c = \\{{{', '.join(map(str, c))}\\}}"})

        a = y[:-1]
        b_coef = []
        d = []

        self.pasos.append({"tipo": "texto", "contenido": "Calculamos los coeficientes aᵢ, bᵢ, cᵢ, dᵢ para cada intervalo"})
        for i in range(n):
            self.pasos.append({"tipo": "texto", "contenido": f"• Intervalo [{x[i]}, {x[i+1]}]"})
            self.pasos.append({"tipo": "formula", "contenido": f"a_{{{i}}} = {self.redondear(a[i])}"})
            b_i = (y[i+1] - y[i]) / h[i] - h[i] * (2*c[i] + c[i+1]) / 3
            b_coef.append(self.redondear(b_i))
            self.pasos.append({"tipo": "formula", "contenido": f"b_{{{i}}} = {self.redondear(b_i)}"})
            self.pasos.append({"tipo": "formula", "contenido": f"c_{{{i}}} = {c[i]}"})
            d_i = (c[i+1] - c[i]) / (3 * h[i])
            d.append(self.redondear(d_i))
            self.pasos.append({"tipo": "formula", "contenido": f"d_{{{i}}} = {self.redondear(d_i)}"})

        # Paso 5: mostrar las ecuaciones S(x) sin simplificar
        self.pasos.append({"tipo": "texto", "contenido": "Ecuaciones finales de los trazadores cúbicos (sin simplificar)"})
        for i in range(n):
            eq = f"S_{{{i}}}(x) = {self.redondear(a[i])} + {b_coef[i]}(x - {x[i]}) + {c[i]}(x - {x[i]})^2 + {d[i]}(x - {x[i]})^3"
            self.pasos.append({"tipo": "formula", "contenido": eq})

        # Paso 6: mostrar las ecuaciones S(x) simplificadas
        self.pasos.append({"tipo": "texto", "contenido": "Ecuaciones finales de los trazadores cúbicos (simplificadas) que pasan por los puntos dados"})
        for i in range(n):
            s_x = a[i] + b_coef[i]*(x_sym - x[i]) + c[i]*(x_sym - x[i])**2 + d[i]*(x_sym - x[i])**3
            s_x_simplificado = simplify(s_x)
            eq_s = f"S_{{{i}}}(x) = {latex(s_x_simplificado)}"
            self.pasos.append({"tipo": "formula", "contenido": eq_s})

        return self.pasos

    def generar_grafica(self):
        x = np.array(self.x_valores)
        y = np.array(self.y_valores)
        from scipy.interpolate import CubicSpline
        cs = CubicSpline(x, y, bc_type='natural')
        x_vals = np.linspace(min(x), max(x), 400)
        y_vals = cs(x_vals)

        plt.figure(figsize=(8, 5))
        plt.plot(x_vals, y_vals, label='Spline Cúbico', color='blue')
        plt.scatter(x, y, color='red', label='Puntos de Entrada')
        plt.title('Trazadores Cúbicos Naturales')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        plt.legend()

        nombre_archivo = f"grafica_trazadores_{uuid.uuid4().hex}.png"
        app_path = apps.get_app_config('Metodos_numericos').path
        ruta_guardado = os.path.join(app_path, 'static', 'trazadores', 'graficas', nombre_archivo)
        os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)

        plt.savefig(ruta_guardado)
        plt.close()

        self.grafica_url = os.path.join('/static/trazadores/graficas/', nombre_archivo)
        return self.grafica_url
