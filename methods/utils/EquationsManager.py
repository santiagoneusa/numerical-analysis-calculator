import sympy as sp
import numpy as np

class EquationsManager:

    @staticmethod
    def parse_function(equation_text):
        x = sp.symbols("x")
        equation_text = equation_text.replace("e^", "exp")
        equation_text = equation_text.replace("^", "**")
        equation = sp.sympify(equation_text)
        return sp.lambdify(x, equation)

    @staticmethod
    def significant_figures_to_tolerance(k):
        """
        Converts the number of significant figures (k) to the relative error tolerance.
        |e| < 5 * 10^(-k)
        """
        return 5 * 10**(-k)

    @staticmethod
    def correct_decimals_to_tolerance(d):
        """
        Converts the number of correct decimals (d) to the absolute error tolerance.
        E <= 0.5 * 10^(-d)
        """
        return 0.5 * 10**(-d)
