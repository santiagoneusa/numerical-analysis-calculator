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
        
        # Construct the Vandermonde matrix A
        A = np.vander(x, increasing=True)
        b = np.array(y)
        
        # Solve for the coefficients using the Vandermonde matrix
        coefficients = np.linalg.solve(A, b)
        
        # Create the polynomial equation string
        polynomial = " + ".join([f"{coeff:.4f}*x^{i}" for i, coeff in enumerate(coefficients)])
        
        # Prepare a table with the results for easier presentation
        table = []
        for i, coeff in enumerate(coefficients):
            table.append([f"x^{i}", f"{coeff:.4f}"])

        # Prepare the data for plotting (even though it's not used for plotting here)
        """ plot_data = {
            'x': x.tolist(),
            'y': y.tolist(),
            'coefficients': coefficients.tolist()
        } """

        # Define the headers for the table
        headers = ['Term', 'Coefficient']

        # Prepare the final response with success response
        response = ResponseManager.success_response(
            table=table,
            message="Vandermonde method calculation completed successfully.",
            headers=headers
        )
        
        response['matrix'] = A.tolist()  # Vandermonde matrix as a list
        response['polynomial'] = polynomial  # Polynomial equation
        response['coefficients'] = coefficients.tolist()  # Coefficients as a list
    

        # Add plot_data to the response dictionary (you can use this for later plotting if needed)
        #response['plot_data'] = plot_data

        return response
    

    @staticmethod
    def newton_divided_difference(x_values, y_values, x_to_interpolate):
        """
        Interpolation method for Newton Divided Difference.

        Parameters:
        x_values : list[float] - List of x values (known points).
        y_values : list[float] - List of y values (known results).
        x_to_interpolate : float - The x value at which to interpolate the polynomial.

        Returns:
        dict - Dictionary with the table, message, headers, plot data, and interpolated value.
        """
        n = len(x_values)

        # Validaciones
        if n != len(y_values):
            raise ValueError("The vectors x and y must have the same length.")
        if n < 2:
            raise ValueError("At least two data points are required for Newton interpolation.")
        if len(set(x_values)) != len(x_values):
            raise ValueError("The x values must be distinct (no duplicates).")
        
        # Ordenar los puntos por x
        sorted_indices = np.argsort(x_values)
        x = np.array(x_values)[sorted_indices]
        y = np.array(y_values)[sorted_indices]

        # Construir la tabla de diferencias divididas
        divided_diff_table = np.zeros((n, n))
        divided_diff_table[:, 0] = y
        for j in range(1, n):
            for i in range(j, n):
                divided_diff_table[i, j] = (
                    divided_diff_table[i, j - 1] - divided_diff_table[i - 1, j - 1]
                ) / (x[i] - x[i - j])

        # Coeficientes del polinomio (primera fila de cada columna)
        coefficients = [divided_diff_table[i, i] for i in range(n)]

        # Construir la función polinómica
        def polynomial_function(value):
            result = coefficients[0]
            product = 1
            for i in range(1, n):
                product *= (value - x[i - 1])
                result += coefficients[i] * product
            return result

        # Evaluar el polinomio en el punto dado
        interpolated_value = polynomial_function(x_to_interpolate)

        # Representación textual del polinomio
        polynomial_str = f"{coefficients[0]:.4f}"
        for i in range(1, n):
            term = f"{coefficients[i]:+.4f}"
            for j in range(i):
                term += f"(x - {x[j]:.4f})"
            polynomial_str += " " + term

        # Preparar la tabla
        table = []
        for i in range(n):
            table.append([
                f"Coefficient for term {i + 1}",
                coefficients[i]
            ])
        table.append(["Interpolated Value", interpolated_value])
        table.append(["Polynomial Expression", polynomial_str])

        headers = ['Description', 'Value']

        # Datos para graficar
        plot_data = {
            'x': x.tolist(),
            'y': y.tolist()
        }

        # Estructura de la respuesta
        response = {
            'table': table,
            'status': 'success',
            'message': f"Newton interpolation completed successfully. Interpolated value at x = {x_to_interpolate} is {interpolated_value}.",
            'headers': headers,
            'plot_data': plot_data,
            'interpolated_value': interpolated_value,
            'polynomial_expression': polynomial_str
        }

        return response


    @staticmethod
    def lagrange(x_values, y_values, x_to_interpolate):
        """
        Interpolation method for Lagrange polynomials.

        Parameters:
        x_values : list[float] - List of x values (known points).
        y_values : list[float] - List of y values (known results).
        x_to_interpolate : float - The x value at which to interpolate the polynomial.

        Returns:
        dict - Dictionary with the table, message, headers, plot data, and interpolated value.
        """
        n = len(x_values)
        if n != len(y_values):
            raise ValueError("The vectors x and y must have the same length.")
        
        # Calculate Lagrange basis polynomials and their coefficients
        coefficients = []
        for i in range(n):
            # Lagrange basis polynomial L_i(x)
            L_i = 1
            for j in range(n):
                if i != j:
                    L_i *= np.poly1d([1, -x_values[j]]) / (x_values[i] - x_values[j])
            
            # Multiply L_i(x) by y_i and collect the terms to find the coefficients
            poly = L_i * y_values[i]
            coefficients.append(poly)

        # Sum all the individual polynomials to get the final polynomial
        final_poly = sum(coefficients)

        # Evaluate the final polynomial at the given x_to_interpolate
        interpolated_value = final_poly(x_to_interpolate)

        # Get the coefficients of the final polynomial
        final_coeffs = final_poly.coefficients

        # Create the table with the coefficients for each basis polynomial and the final polynomial
        table = []
        for i in range(n):
            L_i_str = f"L_{i}(x) = "
            terms = [f"{coef} * (x - {x_values[j]})" for j, coef in enumerate(coefficients[i].coefficients)]
            L_i_str += ' + '.join(terms)
            table.append([L_i_str, y_values[i]])

        table.append(["Final Polynomial", "y = " + ' + '.join([f"{coef}x^{len(final_coeffs)-i-1}" for i, coef in enumerate(final_coeffs)])])

        # Include interpolated value in the table
        table.append(["Interpolated Value at x = " + str(x_to_interpolate), interpolated_value])

        headers = ['Basis Polynomial', 'y_i']

        # Prepare the plot data (just the x and y values for plotting)
        plot_data = {
            'x': x_values,
            'y': y_values
        }

        # Response message and structure
        response = {
            'table': table,
            'message': f"Lagrange interpolation completed successfully. Interpolated value at x = {x_to_interpolate} is {interpolated_value}.",
            'headers': headers,
            'plot_data': plot_data,
            'interpolated_value': interpolated_value
        }

        return response

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
        
        if n < 2:
            raise ValueError("At least two data points are required for linear spline interpolation.")

        # Validate that x_values are in ascending order
        if x_values != sorted(x_values):
            raise ValueError("The x values must be in ascending order.")

        # Validate that x_values are distinct
        if len(set(x_values)) != len(x_values):
            raise ValueError("The x values must be distinct (no duplicates).")

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
        
        if n < 2:
            raise ValueError("At least two data points are required for quadratic spline interpolation.")

        # Validate that x_values are in ascending order
        if x_values != sorted(x_values):
            raise ValueError("The x values must be in ascending order.")

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
        
        if n < 2:
            raise ValueError("At least two data points are required for cubic spline interpolation.")

        # Validate that x_values are in ascending order
        if x_values != sorted(x_values):
            raise ValueError("The x values must be in ascending order.")

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

