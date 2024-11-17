import sympy as sp


class EquationsManager:

    @staticmethod
    def parse_function(equation_text):
        x = sp.symbols("x")
        equation_text = equation_text.replace("e^", "exp")
        equation_text = equation_text.replace("^", "**")
        equation = sp.sympify(equation_text)
        return sp.lambdify(x, equation)
