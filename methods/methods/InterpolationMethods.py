import numpy as np
from methods.utils.ResponseManager import ResponseManager

class InterpolationMethods:

    @staticmethod
    def vandermonde():
        pass

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
