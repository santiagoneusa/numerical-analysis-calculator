import numpy as np
from methods.utils.ResponseManager import ResponseManager

class SystemsEquationsMethods:

    @staticmethod
    def direct_factorization_lu_simple():
        pass

    @staticmethod
    def direct_factorization_lu_partial():
        pass

    @staticmethod
    def croult():
        pass

    @staticmethod
    def doolittle():
        pass

    @staticmethod
    def cholesky():
        pass

    @staticmethod
    def jacobi():
        pass

    @staticmethod
    def gauss_seidel(A, B, tolerance, iterations_limit):
        """
        Método de Gauss-Seidel para resolver sistemas de ecuaciones lineales.

        Parámetros:
        A : list[list[float]] - Matriz de coeficientes.
        B : list[float] - Vector de resultados.
        tolerance : float - Tolerancia para la convergencia.
        iterations_limit : int - Número máximo de iteraciones.

        Retorna:
        list[float] - Solución aproximada para el sistema.
        """
        # Inicializamos el vector X con ceros
        X = [0.0] * len(B)
        iteration = 0
        error = float('inf')  # El error inicial es infinito

        # Creamos una lista para almacenar las soluciones de cada iteración
        table = []

        while iteration < iterations_limit and error > tolerance:
            X_old = X.copy()  # Guardamos el vector de soluciones de la iteración anterior
            for i in range(len(A)):
                # Calculamos la suma de los términos conocidos de la ecuación
                sum_ = sum(A[i][j] * X[j] for j in range(len(A)) if j != i)
                # Actualizamos la incógnita X[i]
                X[i] = (B[i] - sum_) / A[i][i]

            # Calculamos el error como la diferencia entre la solución actual y la anterior
            error = max(abs(X[i] - X_old[i]) for i in range(len(X)))

            # Guardamos el estado de la solución en la tabla para cada iteración
            table.append([iteration + 1] + X + [error])

            iteration += 1

        if error <= tolerance:
            return ResponseManager.success_response(table)
        else:
            return ResponseManager.warning_response(table)

    @staticmethod
    def sor():
        pass
