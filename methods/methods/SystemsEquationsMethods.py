import numpy as np
from methods.utils.ResponseManager import ResponseManager

class SystemsEquationsMethods:

    @staticmethod
    def jacobi(x0, A, b, Tol, niter):
        counter = 0
        error = Tol + 1
        n = len(A)
        x = x0.copy()
        errors = []
        table = []

        # Precomputar D, L y U (Jacobi usa sólo D y el resto como un conjunto)
        D = np.diag(np.diag(A))
        R = A - D  # R = L + U, donde L es la parte inferior y U es la superior de la matriz

        while error > Tol and counter < niter:
            x_new = np.zeros_like(x)  # Inicializar nueva aproximación
            for i in range(n):
                # Calcular la nueva x[i] considerando todo R
                sum_R = sum(R[i][j] * x[j] for j in range(n))
                x_new[i] = (b[i] - sum_R) / A[i][i]

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
    def gauss_seidel(A, b, x0, Tol, niter):
        """
        Método de Gauss-Seidel para resolver sistemas de ecuaciones lineales.

        Parámetros:
        A : list[list[float]] - Matriz de coeficientes.
        b : list[float] - Vector del lado derecho.
        x0 : list[float] - Aproximación inicial.
        Tol : float - Tolerancia para la convergencia.
        niter : int - Número máximo de iteraciones.

        Retorna:
        dict - Contiene el estado (éxito o advertencia), mensaje, encabezados, tabla de iteraciones, solución y errores.
        """
        counter = 0
        error = Tol + 1
        n = len(A)
        x = np.array(x0, dtype=float)  # Convertir x0 a un array de numpy para manipulación
        errors = []
        table = []

        while error > Tol and counter < niter:
            x_new = x.copy()  # Hacemos una copia para evitar modificar x mientras lo usamos
            for i in range(n):
                # Sumar las contribuciones anteriores y posteriores
                sum1 = sum(A[i][j] * x_new[j] for j in range(i))  # i-th row, before i-th element
                sum2 = sum(A[i][j] * x[j] for j in range(i + 1, n))  # i-th row, after i-th element
                # Actualizar la solución para x[i]
                x_new[i] = (b[i] - sum1 - sum2) / A[i][i]

            # Calcular el error relativo
            relative_error_vector = np.abs((x_new - x) / x_new)
            error = np.linalg.norm(relative_error_vector, np.inf)  # Calculamos el error infinito
            errors.append(error)

            counter += 1
            x = x_new.copy()  # Actualizamos x con la nueva solución

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
    def sor(x0, A, b, Tol, niter, w, error_type='relative'):
        """
        Method of Successive Over-Relaxation (SOR) for solving systems of linear equations.

        Parameters:
        x0 : list[float] - Initial guess for the solution.
        A : list[list[float]] - Coefficient matrix.
        b : list[float] - Right-hand side vector.
        Tol : float - Tolerance for convergence.
        niter : int - Maximum number of iterations.
        w : float - Relaxation parameter.
        error_type : str - Type of error to calculate ('relative' or 'absolute').

        Returns:
        dict - Contains status, message, headers, table, solution, errors, and plot data if applicable.
        """
        counter = 0
        error = float('inf')
        n = len(A)
        x = x0.copy()
        errors = []
        table = []

        # For plotting purposes if A is 2x2
        plot_data = None
        if n == 2:
            plot_points = [x.copy()]  # Store the initial guess

        while error > Tol and counter < niter:
            x_new = x.copy()
            for i in range(n):
                sum1 = sum(A[i][j] * x_new[j] for j in range(i))
                sum2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
                x_new[i] = (1 - w) * x[i] + (w / A[i][i]) * (b[i] - sum1 - sum2)

            # Calculate the error based on the selected error type
            if error_type == 'relative':
                # Avoid division by zero
                denominator = np.where(x_new != 0, x_new, np.finfo(float).eps)
                relative_error_vector = np.abs((x_new - x) / denominator)
                error = np.linalg.norm(relative_error_vector, np.inf)
            else:  # Absolute error
                absolute_error_vector = np.abs(x_new - x)
                error = np.linalg.norm(absolute_error_vector, np.inf)

            errors.append(error)
            counter += 1
            x = x_new.copy()
            # Add data to the table
            table.append([counter, x.copy(), error])

            # Collect plot points if A is 2x2
            if n == 2:
                plot_points.append(x.copy())

        if error <= Tol:
            message = f"The method converged in {counter} iterations."
            status = 'success'
        else:
            message = f"The method did not converge in {niter} iterations."
            status = 'warning'

        headers = ['Iteration', 'x', 'Error']

        result = {
            'status': status,
            'message': message,
            'table_headers': headers,
            'table': table,
            'solution': x,
            'errors': errors,
        }

        # If A is 2x2, prepare plot data
        if n == 2:
            result['plot_data'] = {
                'A': A,
                'b': b,
                'iterations': plot_points,
            }

        return result
