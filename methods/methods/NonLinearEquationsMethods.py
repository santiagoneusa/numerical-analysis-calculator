import numpy as np
from methods.utils.ResponseManager import ResponseManager


class NonLinearEquationsMethods:

    @staticmethod
    def bisection(a, b, function, tolerance, iterations_limit):
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

        iteration = 0  # Comenzamos desde 0
        error = None  # Inicializamos el error como None
        c = a  # Inicializamos c con cualquier valor
        table = []

        while iteration < iterations_limit:
            c_old = c
            c = (a * function(b) - b * function(a)) / (function(b) - function(a))
            fc = function(c)

            # En la primera iteración, no podemos calcular el error de forma normal
            if iteration > 0:
                error = abs(c - c_old)
            else:
                error = 100  # Valor arbitrario para la primera iteración

            table.append([iteration + 1, a, b, c, fc, error])

            if fc == 0 or error <= tolerance:
                break

            # Actualizamos los límites
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
    def newton_raphson():
        pass

    @staticmethod
    def secant():
        pass

    @staticmethod
    def multiple_roots_v1():
        pass

    @staticmethod
    def multiple_roots_v2():
        pass
