import sympy as sp

class MathEquationsManager():
    
    @staticmethod
    def parse_function(equation_text):
        x = sp.symbols('x')
        equation_text = equation_text.replace('e^', 'exp')
        equation_text = equation_text.replace('^', '**')
        equation = sp.sympify(equation_text)
        return sp.lambdify(x, equation) 
    
    @staticmethod
    def get_tolerance(decimals):
        function = MathEquationsManager.parse_function('0.5*10^(-x)')
        return function(decimals)
