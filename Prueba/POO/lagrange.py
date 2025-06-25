import sympy as sym
from sympy import Rational, Symbol, expand, latex

class LagrangeSolver:
    def __init__(self, x, y):
        self.x = [Rational(val) for val in x]
        self.y = [Rational(val) for val in y]
        self.n = len(x)
        self.x_eval = Symbol("x")
        self.pasos = []
        self.polinomio_expandido = None 

    def construir_polinomio(self):
        x = self.x
        y = self.y
        x_eval = self.x_eval
        n = self.n
        pasos = self.pasos

        pasos.append({"tipo": "texto", "contenido": "Valores ingresados:"})
        pasos.append({"tipo": "formula", "contenido": f"x = \\{{{', '.join(map(str, x))}\\}}"})
        pasos.append({"tipo": "formula", "contenido": f"y = \\{{{', '.join(map(str, y))}\\}}"})

        polinomio = 0
        for i in range(n):
            Li = 1
            texto_li = []
            for j in range(n):
                if i != j:
                    num = x_eval - x[j]
                    den = x[i] - x[j]
                    Li *= num / den
                    texto_li.append(f"\\frac{{x - {x[j]}}}{{{x[i]} - {x[j]}}}")
            pasos.append({"tipo": "formula", "contenido": f"L_{{{i}}}(x) = {' '.join(texto_li)}"})
            polinomio += y[i] * Li

        polinomio_expandido = expand(polinomio)
        self.polinomio_expandido = polinomio_expandido  
        pasos.append({"tipo": "formula", "contenido": f"P(x) = {sym.latex(polinomio_expandido)}"})

        return pasos
