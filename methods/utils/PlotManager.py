import json
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from methods.methods.InterpolationMethods import InterpolationMethods

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
    def plot_newton_divided_difference(x_values, y_values, polynomial_function):
        # Prepare the plot
        fig, ax = plt.subplots()
        ax.plot(x_values, y_values, 'o', label='Given points', color='red')

        x_dense = np.linspace(min(x_values), max(x_values), 1000)
        y_dense = [polynomial_function(xi) for xi in x_dense]
        ax.plot(x_dense, y_dense, '-', label='Interpolating Polynomial')

        ax.legend()
        ax.grid()

        # Save the figure as a base64 encoded string
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')

        return img_base64
    

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