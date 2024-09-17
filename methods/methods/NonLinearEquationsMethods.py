import numpy as np
from methods.utils.ResponseManager import ResponseManager

class NonLinearEquationsMethods():

    @staticmethod
    def bisection(a, b, function, tolerance, iterations_limit):
        if function(a) * function(b) >= 0:
            raise ValueError("The function must have opposite signs at a and b")
        
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

            if fc == 0: break

            if function(a) * fc >= 0: a = c
            else: b = c            
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
    def secant():
        pass

    @staticmethod
    def multiple_roots_v1():
        pass

    @staticmethod
    def multiple_roots_v2():
        pass
