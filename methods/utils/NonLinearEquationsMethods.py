import numpy as np

class NonLinearEquationsMethods():

    @staticmethod
    def bisection(a, b, function, tolerance, iterations_limit):
        if function(a) * function(b) >= 0:
            raise ValueError("The function must have opposite signs at a and b")
        
        if function(a) == 0:
            return {
                'status': '',
                'message': f'The solution was found on x = {a} with a value of f(x) = {function(a)}',
                'function': function,
                'table': [[0, a, function(a), 0]],
            }
        
        if function(b) == 0:
            return {
                'status': '',
                'message': f'The solution was found on x = {b} with a value of f(x) = {function(b)}',
                'function': function,
                'table': [[0, b, function(b), 0]],
            }
        
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
            return {
                'status': 'warning',
                'message': 'The iterations limit was reached',
                'function': function,
                'table': table,
            }

        return {
            'status': '',
            'message': f'The solution was found on x = {table[iteration-1][1]} with a value of f(x) = {table[iteration-1][2]}',
            'function': function,
            'table': table,
        }
            
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