import sympy as sp
import numpy as np
import math

class EquationsManager:

    @staticmethod
    def parse_function(equation_text):
        x = sp.symbols("x")
        equation_text = equation_text.replace('^', '**')
        equation_text = equation_text.replace('e^', 'exp')
        # Replace 'ln' with 'log' for natural logarithm
        equation_text = equation_text.replace('ln', 'log')
        # Ensure that mathematical functions are correctly interpreted
        # You can add more replacements if needed
        try:
            # Parse the equation using sympy
            equation = sp.sympify(equation_text)
            # Create a lambda function using numpy modules
            return sp.lambdify(x, equation, modules=['numpy'])
        except Exception as e:
            raise ValueError(f"Error parsing the function: {e}")

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

    @staticmethod
    def is_valid_number(value):
        return isinstance(value, (int, float)) and not math.isnan(value) and not math.isinf(value)