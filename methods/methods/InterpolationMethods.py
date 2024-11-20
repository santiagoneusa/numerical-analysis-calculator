import numpy as np
from methods.utils.ResponseManager import ResponseManager

class InterpolationMethods:

    @staticmethod
    def vandermonde(x_values, y_values):
        
        n = len(x_values)
        if n != len(y_values):
            raise ValueError("The vectors x and y must have the same length.")

        # Sort the points by x to avoid problems
        sorted_indices = np.argsort(x_values)
        x = np.array(x_values)[sorted_indices]
        y = np.array(y_values)[sorted_indices]
        
        
        
        

    @staticmethod
    def newton_divided_difference():
        pass

    @staticmethod
    def lagrange(x_values, y_values, x):
        """
        Método de Interpolación de Lagrange.

        Parámetros:
        x_values : list[float] - Lista de los valores de x (puntos conocidos).
        y_values : list[float] - Lista de los valores de y (resultados conocidos).
        x : float - El valor en el que se desea evaluar el polinomio interpolante.

        Retorna:
        float - El valor interpolado de la función en x.
        """
        n = len(x_values)
        result = 0.0
        
        # Calculamos la interpolación de Lagrange
        for i in range(n):
            # Calcular el término L_i(x)
            term = y_values[i]
            for j in range(n):
                if i != j:
                    term *= (x - x_values[j]) / (x_values[i] - x_values[j])
            result += term
        
        return result


    @staticmethod
    def spline_linear(x_values, y_values):
        """
        Interpolation method for linear splines.

        Parameters:
        x_values : list[float] - List of x values (known points).
        y_values : list[float] - List of y values (known results).

        Returns:
        dict - Dictionary with the table, message, headers and plot data.
        """
        n = len(x_values)
        if n != len(y_values):
            raise ValueError("The vectors x and y must have the same length.")

        # Sort the points by x to avoid problems
        sorted_indices = np.argsort(x_values)
        x = np.array(x_values)[sorted_indices]
        y = np.array(y_values)[sorted_indices]

        coefficients = []

        for i in range(n - 1):
            a_i = (y[i + 1] - y[i]) / (x[i + 1] - x[i])  # Slope
            b_i = y[i] - a_i * x[i]                       # Intersection
            coefficients.append([a_i, b_i])

        table = []
        for i in range(len(coefficients)):
            interval = f"[{x[i]}, {x[i+1]}]"
            a_i, b_i = coefficients[i]
            equation = f"y = {a_i} * x + {b_i}"
            table.append([interval, a_i, b_i, equation])

        # Prepare the data for plotting
        plot_data = {
            'x': x.tolist(),
            'y': y.tolist(),
            'coefficients': coefficients
        }

        headers = ['Interval', 'Slope (a_i)', 'Intersection (b_i)', 'Equation']

        response = ResponseManager.success_response(
            table=table,
            message="Calculation completed successfully.",
            headers=headers
        )

        # Add plot_data to the response dictionary
        response['plot_data'] = plot_data

        return response

    @staticmethod
    def spline_quadratic(x_values, y_values):
        """
        Interpolation method for quadratic splines.

        Parameters:
        x_values : list[float] - List of x values (known points).
        y_values : list[float] - List of y values (known results).

        Returns:
        dict - Dictionary with the table, message, headers, and plot data.
        """
        n = len(x_values)
        if n != len(y_values):
            raise ValueError("The vectors x and y must have the same length.")

        # Sort the points by x to avoid problems
        sorted_indices = np.argsort(x_values)
        x = np.array(x_values)[sorted_indices]
        y = np.array(y_values)[sorted_indices]

        num_intervals = n - 1
        num_equations = 3 * num_intervals  # Total number of equations and unknowns

        A = np.zeros((num_equations, num_equations))
        b = np.zeros(num_equations)

        equation = 0  # Equation counter

        # 1. Interpolation conditions (2(n-1) equations)
        for i in range(num_intervals):
            # At x_i: S_i(x_i) = y_i
            A[equation, 3*i] = x[i]**2      # a_i * x_i^2
            A[equation, 3*i + 1] = x[i]     # b_i * x_i
            A[equation, 3*i + 2] = 1        # c_i
            b[equation] = y[i]
            equation += 1

            # At x_{i+1}: S_i(x_{i+1}) = y_{i+1}
            A[equation, 3*i] = x[i+1]**2
            A[equation, 3*i + 1] = x[i+1]
            A[equation, 3*i + 2] = 1
            b[equation] = y[i+1]
            equation += 1

        # 2. First derivative continuity conditions ((n-2) equations)
        for i in range(1, num_intervals):
            # S_i'(x_{i}) = S_{i+1}'(x_{i})
            # Derivative of S_i at x_{i+1} (which is x_{i} for next spline)
            A[equation, 3*(i-1)] = 2 * x[i]      # 2a_{i-1} * x_i
            A[equation, 3*(i-1) + 1] = 1         # b_{i-1}
            # Subtract derivative of S_{i+1} at x_{i}
            A[equation, 3*i] = -2 * x[i]         # -2a_i * x_i
            A[equation, 3*i + 1] = -1            # -b_i
            b[equation] = 0
            equation += 1

        # 3. Second derivative condition at the first point (1 equation)
        # S_1''(x_0) = 0
        A[equation, 0] = 2        # 2a_0
        A[equation, 1] = 0        # Derivative of b_0 is zero
        A[equation, 2] = 0        # Derivative of c_0 is zero
        b[equation] = 0
        equation += 1

        # Solve the system
        coefficients = np.linalg.solve(A, b)

        # Organize the coefficients
        spline_coefficients = []
        for i in range(num_intervals):
            a_i = coefficients[3*i]
            b_i = coefficients[3*i + 1]
            c_i = coefficients[3*i + 2]
            spline_coefficients.append([a_i, b_i, c_i])

        # Prepare the table
        table = []
        for i in range(num_intervals):
            interval = f"[{x[i]}, {x[i+1]}]"
            a_i, b_i, c_i = spline_coefficients[i]
            equation_str = f"S_{i}(x) = {a_i}*x^2 + {b_i}*x + {c_i}"
            table.append([interval, a_i, b_i, c_i, equation_str])

        headers = ['Interval', 'a_i', 'b_i', 'c_i', 'Equation']

        # Prepare the data for plotting
        plot_data = {
            'x': x.tolist(),
            'y': y.tolist(),
            'coefficients': spline_coefficients
        }

        response = ResponseManager.success_response(
            table=table,
            message="Quadratic spline calculation completed successfully.",
            headers=headers
        )

        # Add plot_data to the response dictionary
        response['plot_data'] = plot_data

        return response
    
    @staticmethod
    def spline_cubic(x_values, y_values):
        """
        Interpolation method for cubic splines.

        Parameters:
        x_values : list[float] - List of x values (known points).
        y_values : list[float] - List of y values (known results).

        Returns:
        dict - Dictionary with the table, message, headers, and plot data.
        """
        n = len(x_values)
        if n != len(y_values):
            raise ValueError("The vectors x and y must have the same length.")

        # Sort the points by x to avoid problems
        sorted_indices = np.argsort(x_values)
        x = np.array(x_values)[sorted_indices]
        y = np.array(y_values)[sorted_indices]

        num_intervals = n - 1
        num_equations = 4 * num_intervals  # Total number of equations and unknowns

        A = np.zeros((num_equations, num_equations))
        b = np.zeros(num_equations)

        equation = 0  # Equation counter

        # 1. Interpolation conditions (2(n-1) equations)
        for i in range(num_intervals):
            # At x_i: S_i(x_i) = y_i
            A[equation, 4*i] = x[i]**3      # a_i * x_i^3
            A[equation, 4*i + 1] = x[i]**2  # b_i * x_i^2
            A[equation, 4*i + 2] = x[i]     # c_i * x_i
            A[equation, 4*i + 3] = 1        # d_i
            b[equation] = y[i]
            equation += 1

            # At x_{i+1}: S_i(x_{i+1}) = y_{i+1}
            A[equation, 4*i] = x[i+1]**3
            A[equation, 4*i + 1] = x[i+1]**2
            A[equation, 4*i + 2] = x[i+1]
            A[equation, 4*i + 3] = 1
            b[equation] = y[i+1]
            equation += 1

        # 2. First derivative continuity ((n-2) equations)
        for i in range(1, num_intervals):
            # S_i'(x_{i}) = S_{i+1}'(x_{i})
            A[equation, 4*(i-1)] = 3 * x[i]**2     # 3a_{i-1} * x_i^2
            A[equation, 4*(i-1) + 1] = 2 * x[i]    # 2b_{i-1} * x_i
            A[equation, 4*(i-1) + 2] = 1           # c_{i-1}
            # Subtract derivative of S_{i+1} at x_{i}
            A[equation, 4*i] = -3 * x[i]**2        # -3a_i * x_i^2
            A[equation, 4*i + 1] = -2 * x[i]       # -2b_i * x_i
            A[equation, 4*i + 2] = -1              # -c_i
            b[equation] = 0
            equation += 1

        # 3. Second derivative continuity ((n-2) equations)
        for i in range(1, num_intervals):
            # S_i''(x_{i}) = S_{i+1}''(x_{i})
            A[equation, 4*(i-1)] = 6 * x[i]      # 6a_{i-1} * x_i
            A[equation, 4*(i-1) + 1] = 2         # 2b_{i-1}
            # Subtract second derivative of S_{i+1} at x_{i}
            A[equation, 4*i] = -6 * x[i]         # -6a_i * x_i
            A[equation, 4*i + 1] = -2            # -2b_i
            b[equation] = 0
            equation += 1

        # 4. Natural spline boundary conditions (2 equations)
        # At x[0], S_0''(x[0]) = 0
        A[equation, 0] = 6 * x[0]      # 6a_0 * x_0
        A[equation, 1] = 2             # 2b_0
        b[equation] = 0
        equation += 1

        # At x[n-1], S_{n-2}''(x[n-1]) = 0
        A[equation, 4*(num_intervals-1)] = 6 * x[-1]     # 6a_{n-2} * x_{n-1}
        A[equation, 4*(num_intervals-1) + 1] = 2         # 2b_{n-2}
        b[equation] = 0
        equation += 1

        # Solve the system
        coefficients = np.linalg.solve(A, b)

        # Organize the coefficients
        spline_coefficients = []
        for i in range(num_intervals):
            a_i = coefficients[4*i]
            b_i = coefficients[4*i + 1]
            c_i = coefficients[4*i + 2]
            d_i = coefficients[4*i + 3]
            spline_coefficients.append([a_i, b_i, c_i, d_i])

        # Prepare the table
        table = []
        for i in range(num_intervals):
            interval = f"[{x[i]}, {x[i+1]}]"
            a_i, b_i, c_i, d_i = spline_coefficients[i]
            equation_str = f"S_{i}(x) = {a_i}*x^3 + {b_i}*x^2 + {c_i}*x + {d_i}"
            table.append([interval, a_i, b_i, c_i, d_i, equation_str])

        headers = ['Interval', 'a_i', 'b_i', 'c_i', 'd_i', 'Equation']

        # Prepare the data for plotting
        plot_data = {
            'x': x.tolist(),
            'y': y.tolist(),
            'coefficients': spline_coefficients
        }

        response = ResponseManager.success_response(
            table=table,
            message="Cubic spline calculation completed successfully.",
            headers=headers
        )

        # Add plot_data to the response dictionary
        response['plot_data'] = plot_data

        return response

