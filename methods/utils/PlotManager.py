import json
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

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