import json
import numpy as np

class PlotManager:
    @staticmethod
    def plot_graph(response_data, function, a: float = None, b: float = None):
        if a is None or b is None:
            a = -10
            b = 10

        x_values = np.linspace(a, b, 1000).tolist()
        y_values = [function(x) for x in x_values]

        aproximate_x = response_data["table"][-1][1]
        aproximate_y = response_data["table"][-1][2]

        return {
            "x": json.dumps(x_values),
            "y": json.dumps(y_values),
            "aproximate_x": aproximate_x,
            "aproximate_y": aproximate_y,
            "function": function,
        }