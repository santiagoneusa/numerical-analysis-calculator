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
    def fixed_point():
        pass

    @staticmethod
    def false_position():
        pass

    @staticmethod
    def newton_raphson():
        pass

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
    def multiple_roots_v1():
        pass

    @staticmethod
    def multiple_roots_v2():
        pass
