import sympy as sp
import numpy as np

class SympyEquationsManager:

    @staticmethod
    def parse_function(equation_text):
        x = sp.symbols('x')

        # Reemplazar operadores para que SymPy pueda interpretarlos
        equation_text = equation_text.replace('^', '**')

        # Definir constantes matemáticas en el diccionario local
        local_dict = {
            'e': np.e,
            'pi': np.pi,
            'exp': sp.exp,
            'sin': sp.sin,
            'cos': sp.cos,
            'tan': sp.tan,
            'sqrt': sp.sqrt,
            'log': sp.log,
            # Agrega más funciones matemáticas si es necesario
        }

        try:
            # Parsear la expresión con las constantes definidas
            f_sym = sp.sympify(equation_text, locals=local_dict)
            f_num = sp.lambdify(x, f_sym, modules=['numpy', local_dict])
            return f_sym, f_num
        except (sp.SympifyError, TypeError) as e:
            raise ValueError(f"Error parsing function: {e}")
