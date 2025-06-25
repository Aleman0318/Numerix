import numpy as np
import sympy as sym
from sympy import Mul, Rational, latex
import matplotlib.pyplot as plt
import os
import uuid
from django.apps import apps
import matplotlib
matplotlib.use('Agg')  # Backend no interactivo que genera solo archivos para que evitemos warnings agresivos en consola que detienen procesos o eso creo jajajaja




class LagrangeSolver:
    def __init__(self, x, y): 
        self.x_valores = [Rational(val) for val in x]
        self.y_valores = [Rational(val) for val in y]
        self.n = len(x)
        self.x = sym.Symbol('x')
        self.pasos = []
        self.coordenadas = []
        self.valores_i = []
        self.valores_j = []
        self.terminosP_x = []
        self.Termvisuales_P_x = []
        self.polinomio_latex = ""
        self.x_plot = []
        self.y_plot = []
        self.grafica_url = None

    def construir_polinomio(self):
        polinomio = 0
        self.coordenadas = [f"({a},{b})" for a, b in zip(self.x_valores, self.y_valores)]
        self.valores_i = list(range(self.n))
        self.valores_j = list(range(self.n))

        self.pasos.append({"tipo": "texto", "contenido": "Los pares de coordenadas ingresadas por el usuario fueron"})
        self.pasos.append({"tipo": "formula", "contenido": latex(" ".join(self.coordenadas))})
        self.pasos.append({"tipo": "texto", "contenido": 'El valor para " n " es'})
        self.pasos.append({"tipo": "formula", "contenido": latex(self.n)})
        self.pasos.append({"tipo": "texto", "contenido": "Los valores para x serán"})
        self.pasos.append({"tipo": "formula", "contenido": latex(self.x_valores)})
        self.pasos.append({"tipo": "texto", "contenido": "Los valores para F(x) serán"})
        self.pasos.append({"tipo": "formula", "contenido": latex(self.y_valores)})
        self.pasos.append({"tipo": "texto", "contenido": 'Los valores para → ⅰ'})
        self.pasos.append({"tipo": "formula", "contenido": latex(self.valores_i)})
        self.pasos.append({"tipo": "texto", "contenido": 'Los valores para → j'})
        self.pasos.append({"tipo": "formula", "contenido": latex(self.valores_j)})

        self.pasos.append({"tipo": "texto", "contenido": "Crearemos las Li(x) siguiendo la siguiente fórmula"})
        self.pasos.append({"tipo": "formula", "contenido": r"L_i(x) = \prod_{\substack{0 \leq j \leq n \\ j \ne i}} \frac{x - x_j}{x_i - x_j}"})

        for i in self.valores_i:
            num = 1
            deno = 1
            self.pasos.append({"tipo": "texto", "contenido": f"◈ ITERACIÓN →  {i+1}"})
            self.pasos.append({"tipo": "texto", "contenido": f"Cálculo de L{i}(x) cuando ⅰ = {i}"})
            for j in self.valores_j:
                if i != j:
                    num *= self.x - self.x_valores[j]
                    deno *= self.x_valores[i] - self.x_valores[j]

            liNatural = num / deno
            self.pasos.append({"tipo": "texto", "contenido": f"Tomamos la expresión L{i}(x) sin expandir el numerador"})
            self.pasos.append({"tipo": "formula", "contenido": latex(liNatural)})

            numExpandido = sym.expand(num)
            denoFraccional = Rational(1 / deno)
            expresion = Mul(denoFraccional, numExpandido, evaluate=False)
            self.pasos.append({"tipo": "texto", "contenido": f"Tomamos la expresión L{i}(x) con el numerador expandido"})
            self.pasos.append({"tipo": "formula", "contenido": latex(expresion)})

            self.pasos.append({"tipo": "texto", "contenido": "Sacamos el denominador como fracción y pasamos a multiplicarlo con el numerador expandido"})
            latex_expr_lx = f" l{i}(x) → \\frac{{1}}{{{deno}}}\\left({latex(numExpandido)}\\right)"
            self.pasos.append({"tipo": "formula", "contenido": latex_expr_lx})

            expresion = Mul(denoFraccional, numExpandido)
            Ter_Px = self.y_valores[i] * expresion
            self.terminosP_x.append(Ter_Px)

            self.Termvisuales_P_x.append(f"{latex(self.y_valores[i])} \\cdot {latex_expr_lx}")

        self.pasos.append({"tipo": "texto", "contenido": "Luego, usamos la fórmula general para construir el polinomio de interpolación:"})
        self.pasos.append({"tipo": "formula", "contenido": r"P(x) = \sum_{i=0}^{n} y_i \cdot L_i(x)"})

        self.pasos.append({"tipo": "texto", "contenido": "Agrupamos los pares de F(x) y Lⅰ(x) para formar P(x)"})
        formula_completa = " + ".join(self.Termvisuales_P_x)
        self.pasos.append({"tipo": "formula", "contenido": formula_completa})

        p_x_completo = sum(self.terminosP_x)
        self.polinomio_latex = latex(p_x_completo)
        self.pasos.append({"tipo": "texto", "contenido": "El polinomio P(x) resultante es:"})
        self.pasos.append({"tipo": "formula", "contenido": f"P(x) = {self.polinomio_latex}"})

        self._generar_grafica(p_x_completo)

        return self.pasos

    def _generar_grafica(self, polinomio_sym):
        f = sym.lambdify(self.x, polinomio_sym, "numpy")
        x_plot = np.linspace(float(self.x_valores[0]) - 1, float(self.x_valores[-1]) + 1, 300)
        y_plot = f(x_plot)

        self.x_plot = list(x_plot)
        self.y_plot = list(y_plot)

        plt.figure(figsize=(8, 5))
        plt.plot(x_plot, y_plot, label='P(x)', color='blue')
        plt.scatter([float(v) for v in self.x_valores], [float(v) for v in self.y_valores], color='red', zorder=5)
        plt.title('Polinomio de Lagrange')
        plt.xlabel('x')
        plt.ylabel('P(x)')
        plt.grid(True)
        plt.legend()
        nombre_archivo = f"grafica_lagrange_{uuid.uuid4().hex}.png"

        # Obtener la ruta de la app Metodos_numericos
        app_path = apps.get_app_config('Metodos_numericos').path

        # Ruta absoluta donde guardar la gráfica
        ruta_guardado = os.path.join(app_path, 'static', 'lagrange', 'graficas', nombre_archivo)
        os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)

        # Guardar la imagen
        plt.savefig(ruta_guardado)
        plt.close()

        # Ruta relativa para usar en el HTML
        self.grafica_url = os.path.join('/static/lagrange/graficas/', nombre_archivo)