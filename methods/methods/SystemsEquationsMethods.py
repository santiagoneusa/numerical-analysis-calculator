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
    def sor(x0, A, b, Tol, niter, w):
        """
        Method of Successive Over-Relaxation (SOR) for solving systems of linear equations.

        Parameters:
        x0 : list[float] - Initial guess for the solution.
        A : list[list[float]] - Coefficient matrix.
        b : list[float] - Right-hand side vector.
        Tol : float - Tolerance for convergence.
        niter : int - Maximum number of iterations.
        w : float - Relaxation parameter.
        """
        counter = 0
        error = Tol + 1
        n = len(A)
        x = x0.copy()
        errors = []
        table = []

        while error > Tol and counter < niter:
            x_new = x.copy()
            for i in range(n):
                sum1 = sum(A[i][j] * x_new[j] for j in range(i))
                sum2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
                x_new[i] = (1 - w) * x[i] + (w / A[i][i]) * (b[i] - sum1 - sum2)
            # Calcular el error relativo
            relative_error_vector = np.abs((x_new - x) / x_new)
            error = np.linalg.norm(relative_error_vector, np.inf)
            errors.append(error)
            counter += 1
            x = x_new.copy()
            # Añadir datos a la tabla
            table.append([counter, x.copy(), error])

        if error < Tol:
            message = f"The method converged in {counter} iterations."
            status = 'success'
        else:
            message = f"The method did not converge in {niter} iterations."
            status = 'warning'

        headers = ['Iteration', 'x', 'Error']
        return {
            'status': status,
            'message': message,
            'table_headers': headers,
            'table': table,
            'solution': x,
            'errors': errors,
        }
