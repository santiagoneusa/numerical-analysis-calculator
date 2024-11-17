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
    def spline_linear():
        pass

    @staticmethod
    def spline_square():
        pass

    @staticmethod
    def spline_cubic():
        pass
