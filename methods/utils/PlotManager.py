import json
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from methods.methods.InterpolationMethods import InterpolationMethods
from io import BytesIO

class PlotManager:
    @staticmethod
    def plot_graph(response_data, function, a: float = None, b: float = None):
        aproximate_x = response_data["table"][-1][1]
        aproximate_y = response_data["table"][-1][2]

        x_values = np.linspace(a, b, 1000).tolist()
        y_values = [function(x) for x in x_values]

        return {
            "x": json.dumps(x_values),
            "y": json.dumps(y_values),
            "aproximate_x": aproximate_x,
            "aproximate_y": aproximate_y,
            "function": function,
        }


    @staticmethod
    def plot_newton_divided_difference(x, y):
        """
        Generate a plot for the Newton Divided Difference interpolation.

        Parameters:
        x : list[float] - List of x values (known points).
        y : list[float] - List of y values (known results).

        Returns:
        str - Base64 encoded image string.
        """
        # Validaciones básicas
        if len(x) != len(y):
            raise ValueError("The x and y lists must have the same length.")
        
        # Crear una figura para graficar
        fig, ax = plt.subplots()

        # Graficar los puntos conocidos
        ax.plot(x, y, 'o', label='Given points', color='red')

        # Función para calcular el polinomio de Newton
        def newton_polynomial(x_vals, x_points, y_points):
            """
            Calculate the Newton polynomial for a given x value and known data points.
            """
            n = len(x_points)
            # Calcular la tabla de diferencias divididas
            divided_diff_table = np.zeros((n, n))
            divided_diff_table[:, 0] = y_points
            for j in range(1, n):
                for i in range(j, n):
                    divided_diff_table[i, j] = (
                        divided_diff_table[i, j - 1] - divided_diff_table[i - 1, j - 1]
                    ) / (x_points[i] - x_points[i - j])
            
            # Extraer coeficientes del polinomio
            coefficients = [divided_diff_table[i, i] for i in range(n)]
            
            # Evaluar el polinomio en los puntos dados
            result = []
            for val in x_vals:
                res = coefficients[0]
                product = 1
                for i in range(1, n):
                    product *= (val - x_points[i - 1])
                    res += coefficients[i] * product
                result.append(res)
            return result

        # Generar un rango denso de valores x para la curva suave
        x_dense = np.linspace(min(x), max(x), 1000)

        # Calcular los valores y correspondientes para el polinomio de Newton
        y_dense = newton_polynomial(x_dense, x, y)

        # Graficar la curva de interpolación de Newton
        ax.plot(x_dense, y_dense, label='Newton Interpolation', color='blue')

        # Añadir etiquetas y título
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Newton Divided Difference Interpolation')

        # Añadir leyenda
        ax.legend()

        # Guardar la figura en un buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_png = buf.getvalue()
        buf.close()
        plt.close(fig)

        # Codificar la imagen a base64 para insertar en HTML
        graphic = base64.b64encode(image_png).decode('utf-8')

        return graphic


    @staticmethod
    def plot_linear_spline(x, y, coefficients):
        fig, ax = plt.subplots()

        # Plot the original points
        ax.plot(x, y, 'o', label='Given points')
        # Plot each linear segment
        for i in range(len(coefficients)):
            a_i, b_i = coefficients[i]
            x_interval = np.linspace(x[i], x[i+1], 100)
            y_interval = a_i * x_interval + b_i
            ax.plot(x_interval, y_interval, label=f'Trayecto {i+1}')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Linear Spline Interpolation')
        ax.legend()

        # Save the figure to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_png = buf.getvalue()
        buf.close()
        plt.close(fig)

        # Encode the image to base64 to insert it into HTML
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')

        return graphic

    @staticmethod
    def plot_quadratic_spline(x, y, coefficients):
        fig, ax = plt.subplots()

        # Plot the original points
        ax.plot(x, y, 'o', label='Given points')

        # Plot each quadratic segment
        for i in range(len(coefficients)):
            a_i, b_i, c_i = coefficients[i]
            x_interval = np.linspace(x[i], x[i+1], 100)
            y_interval = a_i * x_interval**2 + b_i * x_interval + c_i
            ax.plot(x_interval, y_interval, label=f'Segment {i+1}')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Quadratic Spline Interpolation')
        ax.legend()

        # Save the figure to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_png = buf.getvalue()
        buf.close()
        plt.close(fig)

        # Encode the image to base64 to insert it into HTML
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')

        return graphic
    
    @staticmethod
    def plot_cubic_spline(x, y, coefficients):
        fig, ax = plt.subplots()

        # Plot the original points
        ax.plot(x, y, 'o', label='Given points')

        # Plot each cubic segment
        for i in range(len(coefficients)):
            a_i, b_i, c_i, d_i = coefficients[i]
            x_interval = np.linspace(x[i], x[i+1], 100)
            y_interval = a_i * x_interval**3 + b_i * x_interval**2 + c_i * x_interval + d_i
            ax.plot(x_interval, y_interval, label=f'Segment {i+1}')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Cubic Spline Interpolation')
    
    @staticmethod
    def plot_lagrange(x, y):
        """
        Generate a plot for the Lagrange interpolation.
        
        Parameters:
        x : list[float] - List of x values (known points).
        y : list[float] - List of y values (known results).
        
        Returns:
        str - Base64 encoded image string.
        """
        # Create a figure for plotting
        fig, ax = plt.subplots()

        # Plot the given points (x, y)
        ax.plot(x, y, 'o', label='Given points', color='red')

        # Define the Lagrange polynomial function
        def lagrange_polynomial(x_vals, x_points, y_points):
            """
            Calculate the Lagrange polynomial for a given x value and known data points.
            """
            result = 0
            n = len(x_points)
            for i in range(n):
                term = y_points[i]
                for j in range(n):
                    if i != j:
                        term *= (x_vals - x_points[j]) / (x_points[i] - x_points[j])
                result += term
            return result

        # Generate a dense range of x values for the smooth curve
        x_dense = np.linspace(min(x), max(x), 1000)

        # Calculate the corresponding y values for the Lagrange polynomial
        y_dense = [lagrange_polynomial(xi, x, y) for xi in x_dense]

        # Plot the Lagrange interpolation curve
        ax.plot(x_dense, y_dense, label='Lagrange Interpolation', color='blue')

        # Add labels and title
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Lagrange Interpolation')

        # Add a legend
        ax.legend()

        # Save the figure to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_png = buf.getvalue()
        buf.close()
        plt.close(fig)

        # Encode the image to base64 to insert it into HTML
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')

        return graphic

    @staticmethod
    def plot_sor_iterations(plot_data):
        """
        Generates an HTML plot for the SOR method when A is 2x2.
        Only plots the two equations and the final solution point.

        Parameters:
        plot_data : dict
            Contains 'A', 'b', and 'iterations' keys.

        Returns:
        str - HTML representation of the plot.
        """
        import plotly.graph_objs as go
        from plotly.offline import plot
        import numpy as np

        A = plot_data['A']
        b = plot_data['b']
        iterations = plot_data['iterations']

        # Extract the final solution point
        final_point = iterations[-1]

        # Extract equations from Ax = b
        # Equation 1: a11*x1 + a12*x2 = b1
        # Equation 2: a21*x1 + a22*x2 = b2

        # Create a range for x1
        x1_min = min(final_point[0], final_point[0]) - 10
        x1_max = max(final_point[0], final_point[0]) + 10
        x1_values = np.linspace(x1_min, x1_max, 400)

        # Avoid division by zero in case A[i][1] is zero
        if A[0][1] != 0:
            x2_eq1 = (b[0] - A[0][0] * x1_values) / A[0][1]
            trace_eq1 = go.Scatter(x=x1_values, y=x2_eq1, mode='lines', name='Equation 1')
        else:
            # Vertical line x = b[0]/A[0][0]
            x_eq1 = b[0] / A[0][0]
            trace_eq1 = go.Scatter(x=[x_eq1, x_eq1], y=[x1_min, x1_max], mode='lines', name='Equation 1')

        if A[1][1] != 0:
            x2_eq2 = (b[1] - A[1][0] * x1_values) / A[1][1]
            trace_eq2 = go.Scatter(x=x1_values, y=x2_eq2, mode='lines', name='Equation 2')
        else:
            # Vertical line x = b[1]/A[1][0]
            x_eq2 = b[1] / A[1][0]
            trace_eq2 = go.Scatter(x=[x_eq2, x_eq2], y=[x1_min, x1_max], mode='lines', name='Equation 2')

        # Final solution point
        trace_final_point = go.Scatter(
            x=[final_point[0]],
            y=[final_point[1]],
            mode='markers',
            name='Final Solution',
            marker=dict(size=10, color='red')
        )

        # Layout
        layout = go.Layout(
            title='SOR Method Final Solution',
            xaxis=dict(title='x1'),
            yaxis=dict(title='x2'),
            showlegend=True
        )

        # Combine traces
        data = [trace_eq1, trace_eq2, trace_final_point]
        fig = go.Figure(data=data, layout=layout)

        # Generate the HTML representation
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)

        return plot_div