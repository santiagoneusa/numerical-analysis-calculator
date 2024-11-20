import numpy as np
import sympy as sp
from methods.utils.ResponseManager import ResponseManager
from methods.utils.SympyEquationsManager import SympyEquationsManager


class NonLinearEquationsMethods:

    @staticmethod
    def bisection(a, b, function, tolerance, iterations_limit):
        """
        Implementation of the bisection method.

        Parameters:
        a : float
            Left endpoint of the interval.
        b : float
            Right endpoint of the interval.
        function : function
            The function to find the root of.
        tolerance : float
            Tolerance that determines when to stop the iteration.
        iterations_limit : int
            Maximum number of iterations allowed.

        Returns:
        A response dictionary containing the status, message, table, etc.
        """
        if function(a) * function(b) >= 0:
            raise ValueError("The function must have opposite signs at f(a) and f(b)")

        if function(a) == 0:
            table = [[0, a, function(a), 0]]
            return ResponseManager.success_response(table)

        if function(b) == 0:
            table = [[0, b, function(b), 0]]
            return ResponseManager.success_response(table)

        iteration = 1
        error = 100
        table = [[0, a, function(a), error]]
        while (iteration < iterations_limit) and (tolerance <= error):
            c = (a + b) / 2
            fc = function(c)
            error = abs(fc - table[iteration - 1][2])
            table.append([iteration, c, fc, error])

            if fc == 0:
                break

            if function(a) * fc >= 0:
                a = c
            else:
                b = c
            iteration += 1

        if iteration == iterations_limit:
            return ResponseManager.warning_response(table)
        else:
            return ResponseManager.success_response(table)

    @staticmethod
    def fixed_point(g_function, initial_guess, tolerance, iterations_limit):
        iteration = 0  # Comenzamos desde 0
        x0 = initial_guess
        error = None  # Inicializamos el error como None
        table = [[0, x0, g_function(x0), error]]  # Agregamos la primera fila

        while iteration < iterations_limit:
            x1 = g_function(x0)
            
            # En la primera iteración, no podemos calcular el error normalmente
            if iteration > 0:
                error = abs(x1 - x0)
            else:
                error = 100  # Establecemos un valor arbitrario para la primera iteración

            table.append([iteration + 1, x1, g_function(x1), error])

            if error <= tolerance:
                break

            x0 = x1  # Actualizamos el valor de x0
            iteration += 1  # Incrementamos la iteración

        if iteration == iterations_limit:
            return ResponseManager.warning_response(table)
        else:
            return ResponseManager.success_response(table)

    @staticmethod
    def false_position(a, b, function, tolerance, iterations_limit):
        if function(a) * function(b) >= 0:
            raise ValueError("The function must have opposite signs at f(a) and f(b)")

        iteration = 0  # Start from 0
        error = None  # Initialize the error as None
        c = a  # Initialize c with any value
        table = []

        while iteration < iterations_limit:
            c_old = c
            c = (a * function(b) - b * function(a)) / (function(b) - function(a))
            fc = function(c)

            # In the first iteration, we cannot calculate the error normally
            if iteration > 0:
                error = abs(c - c_old)
            else:
                error = 100  # Arbitrary value for the first iteration

            table.append([iteration + 1, a, b, c, fc, error])

            if fc == 0 or error <= tolerance:
                break

            # Update the limits
            if function(a) * fc < 0:
                b = c
            else:
                a = c

            iteration += 1  # Incrementamos la iteración

        if iteration == iterations_limit:
            return ResponseManager.warning_response(table)
        else:
            return ResponseManager.success_response(table)

    @staticmethod
    def newton_raphson(function_text, x0, tol, iterations_limit, error_type='relative'):
        """
        Implementation of the Newton-Raphson method.

        Parameters:
        function_text : str
            The function f(x) entered by the user as a string of text.
        x0 : float
            Initial approximation of the root.
        tol : float
            Tolerance that determines when to stop the iteration.
        iterations_limit : int
            Maximum number of iterations allowed.
        error_type : str
            Type of error to calculate ('relative' or 'absolute').

        Returns:
        A response dictionary containing the status, message, table, etc.
        """

        x = sp.symbols('x')

        # Parsear la función y calcular su derivada
        try:
            f_sym, f_num = SympyEquationsManager.parse_function(function_text)
            df_sym = sp.diff(f_sym, x)
            df_num = sp.lambdify(x, df_sym, modules=['numpy'])
        except Exception as e:
            return ResponseManager.error_response(f"Error parsing the function or its derivative: {e}")
        

        # Initialize variables
        x_i = x0
        error = float('inf')
        iterations = 0
        prev_x_i = None
        table = []

        # Start of iterations
        while error > tol and iterations < iterations_limit:
            try:
                f_x_i = f_num(x_i)
                df_x_i = df_num(x_i)
                
            except Exception as e:
                return ResponseManager.error_response(f"Error evaluating the function or its derivative: {e}")

            if df_x_i == 0:
                return ResponseManager.error_response(f"The derivative is zero at x = {x_i}. Cannot continue.")

            new_x_i = x_i - f_x_i / df_x_i

            # Calculate the error
            if iterations > 0:
                if error_type == 'relative' and new_x_i != 0:
                    error = abs((new_x_i - prev_x_i) / new_x_i)
                else:
                    error = abs(new_x_i - prev_x_i)
            else:
                error = float('inf')

            # Agregar datos a la tabla
            table.append([iterations, x_i, f_x_i, df_x_i, error])

            # Preparar para la siguiente iteración
            prev_x_i = x_i
            x_i = new_x_i
            iterations += 1

        # Prepare the response
        if abs(f_x_i) <= tol or error <= tol:
            message = f"An approximate root is x = {x_i} with f(x) = {f_x_i}"
            return ResponseManager.success_response(table, message)
        else:
            message = f"The method did not converge after {iterations_limit} iterations."
            return ResponseManager.warning_response(table, message)

    @staticmethod
    def secant(x0, x1, function, tolerance, iterations_limit):
        table = []
        iteration = 0
        error = float('inf')

        fx0 = function(x0)
        fx1 = function(x1)

        if fx0 == fx1:
            raise ValueError("Division by zero! f(x0) and f(x1) cannot be the same.")

        table.append([iteration, x0, fx0, "N/A"])
        iteration += 1
        table.append([iteration, x1, fx1, abs((x1 - x0) / x1)])

        while iteration < iterations_limit and error > tolerance:
            if fx0 == fx1:
                raise ValueError("Division by zero encountered during iterations.")

            x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
            fx2 = function(x2)

            if x2 != 0:
                error = abs((x2 - x1) / x2)
            else:
                error = float('inf')

            iteration += 1
            table.append([iteration, x2, fx2, error])

            x0, x1 = x1, x2
            fx0, fx1 = fx1, fx2

            if error < tolerance or fx2 == 0:
                break

        if iteration == iterations_limit:
            return ResponseManager.warning_response(table)
        else:
            return ResponseManager.success_response(table)

    @staticmethod
    def multiple_roots_v1(x0, tol, iterations_limit, multi, function ):
        
        """
        Using multiplicity
        """
        
        x_symbol = sp.symbols('x')

        # Parsear la función y calcular su derivada
        try:
            f_sym = sp.sympify(function.replace('^', '**'))
        except (sp.SympifyError, TypeError) as e:
            return ResponseManager.error_response(f"Error interpreting the function: {e}")
        
        f_num = sp.lambdify(x_symbol, f_sym, 'numpy')

        df_sym = sp.diff(f_sym, x_symbol)
        df_num = sp.lambdify(x_symbol, df_sym, 'numpy')
        
        # Initialize lists and variables
        xn = []
        x = x0
        f = f_num(x)
        derivada = df_num(x)
        iteration = 0
        Error = float('inf')  # Initial error set to a high value
        xn.append(x)
        table = []
        
        while Error > tol and f != 0 and derivada != 0 and iteration < iterations_limit:
            x = x - multi*(f / derivada)
            derivada = df_num(x)
            f = f_num(x)
            xn.append(x)
            iteration += 1
            Error = abs(xn[iteration] - xn[iteration - 1])
            table.append([iteration, x, f, Error])
                 
        if iteration == iterations_limit:
            return ResponseManager.warning_response(table)
        else:
            return ResponseManager.success_response(table)
            
            
        

    @staticmethod
    def multiple_roots_v2(x0, tol, iterations_limit, function):
        
        x_symbol = sp.symbols('x')

        # Parsear la función y calcular su derivada
        try:
            f_sym = sp.sympify(function.replace('^', '**'))
        except (sp.SympifyError, TypeError) as e:
            return ResponseManager.error_response(f"Error interpreting the function: {e}")
        
        f_num = sp.lambdify(x_symbol, f_sym, 'numpy')

        df_sym = sp.diff(f_sym, x_symbol)
        df_num = sp.lambdify(x_symbol, df_sym, 'numpy')
        
        df2_sym = sp.diff(f_sym, x_symbol, 2)
        df2_num = sp.lambdify(x_symbol, df2_sym, 'numpy')
        
        # Initialize lists and variables
        xn = []
        x = x0
        f = f_num(x)
        derivada = df_num(x)
        segunda_derivada = df2_num(x)
        iteration = 0
        Error = float('inf')  # Initial error set to a high value
        xn.append(x)
        table = []
        
        while Error > tol and f != 0  and iteration < iterations_limit:
            x = x - ( f * derivada / derivada**2 - (f*segunda_derivada))
            derivada = df_num(x)
            segunda_derivada = df2_num(x)
            f = f_num(x)
            xn.append(x)
            iteration += 1
            Error = abs(xn[iteration] - xn[iteration - 1])
