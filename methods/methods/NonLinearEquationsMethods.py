import numpy as np
import sympy as sp
from methods.utils.ResponseManager import ResponseManager
from methods.utils.SympyEquationsManager import SympyEquationsManager
from methods.utils.EquationsManager import EquationsManager


class NonLinearEquationsMethods:

    @staticmethod
    def bisection(a, b, function, tolerance, iterations_limit, error_type='relative'):
        """
        Implementation of the Bisection Method with error type selector.

        Parameters:
        a : float
            Left endpoint of the interval.
        b : float
            Right endpoint of the interval.
        function : callable
            The function to find the root of.
        tolerance : float
            Tolerance that determines when to stop the iteration.
        iterations_limit : int
            Maximum number of iterations allowed.
        error_type : str
            Type of error to calculate ('relative' or 'absolute').

        Returns:
        A response dictionary containing the status, message, table, etc.
        """

        # Input validation
        if not EquationsManager.is_valid_number(a):
            return ResponseManager.error_response("Left endpoint a must be a valid number.")

        if not EquationsManager.is_valid_number(b):
            return ResponseManager.error_response("Right endpoint b must be a valid number.")

        if not EquationsManager.is_valid_number(tolerance) or tolerance <= 0:
            return ResponseManager.error_response("Tolerance must be a positive number.")

        if not isinstance(iterations_limit, int) or iterations_limit <= 0:
            return ResponseManager.error_response("Iterations limit must be a positive integer.")

        if error_type not in ('relative', 'absolute'):
            return ResponseManager.error_response("Error type must be 'relative' or 'absolute'.")

        try:
            fa = function(a)
            fb = function(b)
        except Exception as e:
            return ResponseManager.error_response(f"Error evaluating the function at endpoints: {e}")

        if fa * fb > 0:
            return ResponseManager.error_response("The function must have opposite signs at a and b.")

        table = []
        iteration = 0
        error = float('inf')
        c = a  # Initial approximation
        fc = fa

        headers = ['Iteration', 'a', 'b', 'c', 'f(c)', 'Error']

        # Start iterations
        while error > tolerance and iteration < iterations_limit:
            c_prev = c  # Store previous c
            c = (a + b) / 2.0
            try:
                fc = function(c)
            except Exception as e:
                return ResponseManager.error_response(f"Error evaluating the function at c = {c}: {e}")

            # Calculate the error
            if iteration == 0:
                error = float('inf')  # No error in the first iteration
            else:
                if error_type == 'relative':
                    if c != 0:
                        error = abs((c - c_prev) / c)
                    else:
                        error = float('inf')
                else:  # Absolute error
                    error = abs(c - c_prev)

            # Append data to the table
            table.append([iteration, a, b, c, fc, error])

            # Check for convergence
            if abs(fc) <= tolerance or error <= tolerance:
                message = f"An approximate root is c = {c} with f(c) = {fc}"
                return ResponseManager.success_response(table, message, headers)

            # Decide the side to repeat the steps
            if fa * fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc

            iteration += 1

        # If the method did not converge within the iteration limit
        message = f"The method did not converge after {iterations_limit} iterations."
        return ResponseManager.warning_response(table, message, headers)


    @staticmethod
    def fixed_point(g_function, initial_guess, tolerance, iterations_limit, error_type='relative'):
        """
        Implementation of the Fixed Point Iteration method.

        Parameters:
        g_function : function
            The function g(x) used to approximate the root.
        initial_guess : float
            Initial approximation of the root.
        tolerance : float
            The tolerance for the stopping condition.
        iterations_limit : int
            The maximum number of iterations allowed.
        error_type : str
            The type of error to calculate ('relative' or 'absolute').

        Returns:
        A response dictionary containing the status, message, table, etc.
        """

        # Validación de entrada
        if not isinstance(iterations_limit, int) or iterations_limit <= 0:
            return ResponseManager.error_response("Iterations limit must be a positive integer.")

        if error_type not in ('relative', 'absolute'):
            return ResponseManager.error_response("Error type must be 'relative' or 'absolute'.")

        # Inicialización de variables
        iteration = 0
        x0 = initial_guess
        error = float('inf')  # Inicializamos el error con un valor grande
        table = []  # Tabla de resultados

        # Agregar la primera iteración
        try:
            g_x0 = g_function(x0)
            table.append([iteration, x0, g_x0, "N/A"])  # No hay error en la primera iteración
        except Exception as e:
            return ResponseManager.error_response(f"Error evaluating the function at x = {x0}: {e}")

        # Comienza la iteración
        while iteration < iterations_limit:
            try:
                x1 = g_function(x0)
            except Exception as e:
                return ResponseManager.error_response(f"Error evaluating the function at x = {x0}: {e}")

            # Calcular el error
            if iteration > 0:
                if error_type == 'relative' and x1 != 0:
                    error = abs((x1 - x0) / x1)  # Error relativo
                else:
                    error = abs(x1 - x0)  # Error absoluto

            # Agregar los datos a la tabla
            try:
                g_x1 = g_function(x1)
                table.append([iteration + 1, x1, g_x1, error])
            except Exception as e:
                return ResponseManager.error_response(f"Error evaluating the function at x = {x1}: {e}")

            # Verificar si el error o g(x1) cumplen la tolerancia
            if error <= tolerance or abs(g_x1) <= tolerance:
                message = f"Converged to a root at x = {x1} with g(x) = {g_x1}"
                headers = ["Iteration", "x_i", "g(x_i)", "Error"]
                return ResponseManager.success_response(table, message, headers)

            # Preparar para la siguiente iteración
            x0 = x1
            iteration += 1

        # Si no convergió después del límite de iteraciones
        message = f"Method did not converge after {iterations_limit} iterations."
        headers = ["Iteration", "x_i", "g(x_i)", "Error"]
        return ResponseManager.warning_response(table, message, headers)
    

    @staticmethod
    def false_position(a, b, function, tolerance, iterations_limit, error_type="relative"):
        """
        Implementation of the False Position (Regula Falsi) method.

        Parameters:
        a : float
            Left boundary of the interval.
        b : float
            Right boundary of the interval.
        function : function
            The function for which we are finding the root.
        tolerance : float
            The tolerance for the stopping condition.
        iterations_limit : int
            The maximum number of iterations allowed.
        error_type : str
            The type of error ('relative' or 'absolute').

        Returns:
        A response dictionary containing the status, message, table, etc.
        """
        if function(a) * function(b) >= 0:
            return ResponseManager.error_response("The function must have opposite signs at f(a) and f(b)")

        iteration = 0  # Start from 0
        error = float('inf')  # Initialize the error as infinity for the first iteration
        c = a  # Initialize c with any value
        table = []

        # First iteration value
        table.append([iteration, a, b, c, function(c), error])

        while iteration < iterations_limit:
            c_old = c
            c = (a * function(b) - b * function(a)) / (function(b) - function(a))
            fc = function(c)

            # Calculate the error
            if iteration > 0:
                if error_type == "relative":
                    error = abs((c - c_old) / c) if c != 0 else float('inf')  # Relative error
                else:  # Absolute error
                    error = abs(c - c_old)
            else:
                error = float('inf')  # Arbitrary value for the first iteration

            # Add to the table
            table.append([iteration + 1, a, b, c, fc, error])

            # Check for convergence or tolerance
            if abs(fc) <= tolerance or error <= tolerance:
                message = f"Converged to a root at x = {c} with f(x) = {fc}"
                headers = ["Iteration", "a", "b", "c", "f(c)", "Error"]
                return ResponseManager.success_response(table, message, headers)

            # Update the interval limits
            if function(a) * fc < 0:
                b = c
            else:
                a = c

            iteration += 1  # Increment iteration

        # If the method did not converge within the iteration limit
        message = f"Method did not converge after {iterations_limit} iterations."
        headers = ["Iteration", "a", "b", "c", "f(c)", "Error"]
        return ResponseManager.warning_response(table, message, headers)

    @staticmethod
    def newton_raphson(function_text, x0, tol, iterations_limit, error_type='relative'):
        """
        Implementation of the Newton-Raphson method with enhanced error handling.

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

        # Input validation
        if not EquationsManager.is_valid_number(x0):
            return ResponseManager.error_response("Initial guess x0 must be a valid number.")

        if not EquationsManager.is_valid_number(tol) or tol <= 0:
            return ResponseManager.error_response("Tolerance must be a positive number.")

        if not isinstance(iterations_limit, int) or iterations_limit <= 0:
            return ResponseManager.error_response("Iterations limit must be a positive integer.")

        if error_type not in ('relative', 'absolute'):
            return ResponseManager.error_response("Error type must be 'relative' or 'absolute'.")

        # Parse the function and its derivative
        try:
            # Replace '^' with '**' for exponentiation
            function_text = function_text.replace('^', '**')
            f_sym = sp.sympify(function_text)
            f_num = sp.lambdify(x, f_sym, modules=['numpy'])
            df_sym = sp.diff(f_sym, x)
            df_num = sp.lambdify(x, df_sym, modules=['numpy'])
        except Exception as e:
            return ResponseManager.error_response(f"Error parsing the function or its derivative: {e}")

        # Initialize variables
        x_i = x0
        iterations = 0
        table = []
        prev_x_i = None  # No previous approximation yet

        # Start of iterations
        while iterations < iterations_limit:
            # Check if x_i is valid
            if not EquationsManager.is_valid_number(x_i):
                return ResponseManager.error_response(f"Current approximation x = {x_i} is not a valid number. Cannot continue.")

            try:
                f_x_i = f_num(x_i)
                df_x_i = df_num(x_i)
            except Exception as e:
                return ResponseManager.error_response(f"Error evaluating the function or its derivative at x = {x_i}: {e}")

            # Check if f_x_i and df_x_i are valid numbers
            if not EquationsManager.is_valid_number(f_x_i):
                return ResponseManager.error_response(f"The function evaluation resulted in an invalid number at x = {x_i} (f(x) = {f_x_i}). Cannot continue.")

            if not EquationsManager.is_valid_number(df_x_i):
                return ResponseManager.error_response(f"The derivative evaluation resulted in an invalid number at x = {x_i} (f'(x) = {df_x_i}). Cannot continue.")

            # Check if f_x_i or df_x_i are complex numbers
            if isinstance(f_x_i, complex):
                return ResponseManager.error_response(f"The function evaluation resulted in a complex number at x = {x_i} (f(x) = {f_x_i}). Cannot continue.")

            if isinstance(df_x_i, complex):
                return ResponseManager.error_response(f"The derivative evaluation resulted in a complex number at x = {x_i} (f'(x) = {df_x_i}). Cannot continue.")

            # Check if derivative is zero
            if df_x_i == 0:
                return ResponseManager.error_response(f"The derivative is zero at x = {x_i}. Cannot continue.")

            # Update x_i
            new_x_i = x_i - f_x_i / df_x_i

            # Check if new_x_i is valid
            if not EquationsManager.is_valid_number(new_x_i):
                return ResponseManager.error_response(f"The new approximation resulted in an invalid number (x = {new_x_i}). Cannot continue.")

            # Calculate the error
            if prev_x_i is None:
                error = 'N/A'  # No error for the first iteration
            else:
                if error_type == 'relative':
                    if new_x_i != 0:
                        error = abs((new_x_i - x_i) / new_x_i)
                    else:
                        error = float('inf')  # Cannot compute relative error when new_x_i is zero
                else:  # Absolute error
                    error = abs(new_x_i - x_i)

                # Check if error is valid
                if not EquationsManager.is_valid_number(error):
                    return ResponseManager.error_response(f"The error calculation resulted in an invalid number (error = {error}). Cannot continue.")

                # Check for convergence
                if abs(f_x_i) <= tol or error <= tol:
                    table.append([iterations, x_i, f_x_i, error])
                    break

            # Add data to the table
            table.append([iterations, x_i, f_x_i, error])

            # Prepare for the next iteration
            prev_x_i = x_i
            x_i = new_x_i
            iterations += 1

        else:
            # If the loop completes without breaking, check if the solution is acceptable
            if abs(f_x_i) > tol:
                message = f"The method did not converge after {iterations_limit} iterations."
                headers = ['Iteration', 'x_i', 'f(x_i)', 'Error']
                return ResponseManager.warning_response(table, message, headers)

        # Prepare the success response
        headers = ['Iteration', 'x_i', 'f(x_i)', 'Error']
        message = f"An approximate root is x = {x_i} with f(x) = {f_x_i}"
        return ResponseManager.success_response(table, message, headers)

    @staticmethod
    def secant(x0, x1, function, tolerance, iterations_limit, error_type='relative'):
        """
        Implementation of the Secant method with enhanced error handling.

        Parameters:
        x0 : float
            First initial approximation of the root.
        x1 : float
            Second initial approximation of the root.
        function : callable
            The function to find the root of.
        tolerance : float
            Tolerance that determines when to stop the iteration.
        iterations_limit : int
            Maximum number of iterations allowed.
        error_type : str
            Type of error to calculate ('relative' or 'absolute').

        Returns:
        A response dictionary containing the status, message, table, etc.
        """
        # Input validation
        if not EquationsManager.is_valid_number(x0):
            return ResponseManager.error_response("Initial approximation x0 must be a valid number.")

        if not EquationsManager.is_valid_number(x1):
            return ResponseManager.error_response("Initial approximation x1 must be a valid number.")

        if not EquationsManager.is_valid_number(tolerance) or tolerance <= 0:
            return ResponseManager.error_response("Tolerance must be a positive number.")

        if not isinstance(iterations_limit, int) or iterations_limit <= 0:
            return ResponseManager.error_response("Iterations limit must be a positive integer.")

        if error_type not in ('relative', 'absolute'):
            return ResponseManager.error_response("Error type must be 'relative' or 'absolute'.")

        table = []
        iteration = 0

        # Evaluate the function at x0 and x1
        try:
            fx0 = function(x0)
            fx1 = function(x1)
        except Exception as e:
            return ResponseManager.error_response(f"Error evaluating the function at initial approximations: {e}")

        # Check if fx0 and fx1 are valid numbers
        if not EquationsManager.is_valid_number(fx0):
            return ResponseManager.error_response(f"Function evaluation at x0 resulted in an invalid number (f(x0) = {fx0}).")

        if not EquationsManager.is_valid_number(fx1):
            return ResponseManager.error_response(f"Function evaluation at x1 resulted in an invalid number (f(x1) = {fx1}).")

        # Check for division by zero before starting iterations
        if fx0 == fx1:
            return ResponseManager.error_response("Division by zero! f(x0) and f(x1) cannot be the same.")

        # Initialize error
        error = 'N/A'  # No error for the first approximation

        # Add initial approximations to the table
        table.append([iteration, x0, fx0, error])
        iteration += 1

        # Calculate initial error for x1
        if error_type == 'relative':
            if x1 != 0:
                error = abs((x1 - x0) / x1)
            else:
                error = float('inf')
        else:
            error = abs(x1 - x0)

        # Add second approximation to the table
        table.append([iteration, x1, fx1, error])

        # Start iterations
        while iteration < iterations_limit:
            if fx0 == fx1:
                return ResponseManager.error_response("Division by zero encountered during iterations (f(x0) == f(x1)).")

            # Compute new approximation
            x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)

            # Evaluate the function at x2
            try:
                fx2 = function(x2)
            except Exception as e:
                return ResponseManager.error_response(f"Error evaluating the function at x = {x2}: {e}")

            # Check if fx2 is a valid number
            if not EquationsManager.is_valid_number(fx2):
                return ResponseManager.error_response(f"Function evaluation resulted in an invalid number at x = {x2} (f(x) = {fx2}).")

            # Calculate the error based on the selected error type
            if error_type == 'relative':
                if x2 != 0:
                    error = abs((x2 - x1) / x2)
                else:
                    error = float('inf')  # Cannot compute relative error when x2 is zero
            else:  # Absolute error
                error = abs(x2 - x1)

            # Add data to the table
            iteration += 1
            table.append([iteration, x2, fx2, error])

            # Check for convergence
            if abs(fx2) <= tolerance or error <= tolerance:
                message = f"An approximate root is x = {x2} with f(x) = {fx2}"
                headers = ['Iteration', 'x', 'f(x)', 'Error']
                return ResponseManager.success_response(table, message, headers)

            # Prepare for next iteration
            x0, x1 = x1, x2
            fx0, fx1 = fx1, fx2

        # If the method did not converge within the iteration limit
        message = f"The method did not converge after {iterations_limit} iterations."
        headers = ['Iteration', 'x', 'f(x)', 'Error']
        return ResponseManager.warning_response(table, message, headers)

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
            x = x - (f * derivada) / (derivada**2 - f * segunda_derivada)
            derivada = df_num(x)
            segunda_derivada = df2_num(x)
    
            f = f_num(x)
            xn.append(x)
            iteration += 1
            Error = abs(xn[iteration] - xn[iteration - 1])
            table.append([iteration, x, f, Error]) 
        

       
        if iteration == iterations_limit:
            return ResponseManager.warning_response(table)
        else:
            return ResponseManager.success_response(table)
        
