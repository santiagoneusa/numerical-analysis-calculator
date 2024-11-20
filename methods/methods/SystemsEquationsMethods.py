import numpy as np
from methods.utils.ResponseManager import ResponseManager

class SystemsEquationsMethods:

    @staticmethod
    def jacobi():
        pass

    @staticmethod
    def gauss_seidel(x0, A, b, Tol, niter):
        """
        Método de Gauss-Seidel para resolver sistemas de ecuaciones lineales.

        Parámetros:
        x0 : list[float] - Aproximación inicial.
        A : list[list[float]] - Matriz de coeficientes.
        b : list[float] - Vector del lado derecho.
        Tol : float - Tolerancia para la convergencia.
        niter : int - Número máximo de iteraciones.

        Retorna:
        dict - Contiene el estado (éxito o advertencia), mensaje, encabezados, tabla de iteraciones, solución y errores.
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
                # Sumar las contribuciones anteriores y posteriores
                sum1 = sum(A[i][j] * x_new[j] for j in range(i))
                sum2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
                # Actualizar la solución para x[i]
                x_new[i] = (b[i] - sum1 - sum2) / A[i][i]

            # Calcular el error relativo
            relative_error_vector = np.abs((x_new - x) / x_new)
            error = np.linalg.norm(relative_error_vector, np.inf)
            errors.append(error)

            counter += 1
            x = x_new.copy()

            # Guardar datos de iteración en la tabla
            table.append([counter, x.copy(), error])

        if error < Tol:
            message = f"El método convergió en {counter} iteraciones."
            status = 'success'
        else:
            message = f"El método no convergió en {niter} iteraciones."
            status = 'warning'

        headers = ['Iteración', 'x', 'Error']
        return {
            'status': status,
            'message': message,
            'table_headers': headers,
            'table': table,
            'solution': x,
            'errors': errors,
        }

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
