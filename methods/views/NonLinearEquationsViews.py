from django.shortcuts import render
from methods.utils.ResponseManager import ResponseManager
from methods.utils.EquationsManager import EquationsManager
from methods.utils.PlotManager import PlotManager
from methods.methods.NonLinearEquationsMethods import NonLinearEquationsMethods
from django.urls import reverse

def bisection(request):
    template_data = {}
    template_data["title"] = "Bisection method"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Non Linear Equations", reverse("home") + "#methods-section"),
        ("Bisection", reverse("methods.bisection")),
    ]

    try:
        if request.POST:
            a = float(request.POST.get("a").replace(',', '.'))
            b = float(request.POST.get("b").replace(',', '.'))
            function_str = request.POST.get("function")
            function = EquationsManager.parse_function(function_str)
            tolerance = float(request.POST.get("correct_decimals").replace(',', '.'))
            iterations_limit = int(request.POST.get("iterations_limit"))

            response = NonLinearEquationsMethods.bisection(a, b, function, tolerance, iterations_limit)
            template_data["response"] = response

            # Obtener la solución aproximada de la respuesta
            approximate_root = response["table"][-1][1]  # Suponiendo que la columna 1 es 'c'

            # Calcular los nuevos límites para la gráfica
            plot_a = approximate_root - 1
            plot_b = approximate_root + 1

            # Verificar que plot_a < plot_b
            if plot_a > plot_b:
                plot_a, plot_b = plot_b, plot_a  # Intercambiar si es necesario

            template_data["plot_data"] = PlotManager.plot_graph(response, function, plot_a, plot_b)

            return render(request, "non_linear_equations/bisection.html", {"template_data": template_data})

        else:
            template_data["response"] = ResponseManager.error_response("All the inputs must have a value.")
            return render(request, "non_linear_equations/bisection.html", {"template_data": template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(str(e))
        return render(request, "non_linear_equations/bisection.html", {"template_data": template_data})


def fixed_point(request):
    template_data = {}
    template_data["title"] = "Fixed Point Method"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Non Linear Equations", reverse("home") + "#methods-section"),
        ("Fixed Point", reverse("methods.fixed_point")),
    ]

    try:
        if request.POST:
            g_function_str = request.POST.get("g_function")
            initial_guess = float(request.POST.get("initial_guess").replace(',', '.'))
            iterations_limit = int(request.POST.get("iterations_limit"))
            error_type = request.POST.get("error_type", "relative")
            tolerance_input = request.POST.get("tolerance").replace(',', '.')

            # Convert tolerance_input to tolerance value
            if error_type == "relative":
                k = int(tolerance_input)
                tolerance = EquationsManager.significant_figures_to_tolerance(k)
            else:
                d = int(tolerance_input)
                tolerance = EquationsManager.correct_decimals_to_tolerance(d)

            # Parseamos la función g(x)
            g_function = EquationsManager.parse_function(g_function_str)

            # Ejecutamos el método de punto fijo
            response = NonLinearEquationsMethods.fixed_point(
                g_function, initial_guess, tolerance, iterations_limit
            )
            template_data["response"] = response

            # Preparar datos para la gráfica
            approximate_root = response["table"][-1][1]
            plot_a = approximate_root - 1
            plot_b = approximate_root + 1
            template_data["plot_data"] = PlotManager.plot_graph(response, g_function, plot_a, plot_b)

            return render(request, "non_linear_equations/fixed_point.html", {"template_data": template_data})
        else:
            return render(request, "non_linear_equations/fixed_point.html", {"template_data": template_data})
    except Exception as e:
        template_data["response"] = ResponseManager.error_response(str(e))
        return render(request, "non_linear_equations/fixed_point.html", {"template_data": template_data})


def false_position(request):
    template_data = {}
    template_data["title"] = "False Position Method"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Non Linear Equations", reverse("home") + "#methods-section"),
        ("False Position", reverse("methods.false_position")),
    ]

    try:
        if request.POST:
            # Obtener datos del formulario
            a = float(request.POST.get("a"))
            b = float(request.POST.get("b"))
            function_str = request.POST.get("function")
            tolerance = float(request.POST.get("tolerance"))
            iterations_limit = int(request.POST.get("iterations_limit"))

            # Parsear la función
            function = EquationsManager.parse_function(function_str)
            
            # Ejecutar el método de falsa posición
            response = NonLinearEquationsMethods.false_position(
                a, b, function, tolerance, iterations_limit
            )

            template_data["response"] = response

            # Preparar datos para la gráfica
            approximate_root = response["table"][-1][3]  # 'c' está en la columna 3
            plot_a = approximate_root - 1
            plot_b = approximate_root + 1
            template_data["plot_data"] = PlotManager.plot_graph(response, function, plot_a, plot_b)

            return render(request, "non_linear_equations/false_position.html", {"template_data": template_data})
        else:
            template_data["response"] = ResponseManager.error_response("All inputs must have a value.")
            return render(request, "non_linear_equations/false_position.html", {"template_data": template_data})
    except Exception as e:
        template_data["response"] = ResponseManager.error_response(str(e))
        return render(request, "non_linear_equations/false_position.html", {"template_data": template_data})



def newton_raphson(request):
    template_data = {}
    template_data["title"] = "Newton-Raphson Method"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Non Linear Equations", reverse("home") + "#methods-section"),
        ("Newton-Raphson", reverse("methods.newton_raphson")),
    ]

    try:
        if request.method == 'POST':
            function_str = request.POST.get("function")
            function = EquationsManager.parse_function(function_str)
            x0 = float(request.POST.get("x0").replace(',', '.'))
            iterations_limit = int(request.POST.get("iterations_limit"))
            error_type = request.POST.get("error_type", "relative")
            tolerance_input = request.POST.get("tolerance").replace(',', '.')

            # Convert tolerance_input to tolerance value
            if error_type == 'relative':
                k = int(tolerance_input)
                tol = EquationsManager.significant_figures_to_tolerance(k)
            else:
                d = int(tolerance_input)
                tol = EquationsManager.correct_decimals_to_tolerance(d)

            response = NonLinearEquationsMethods.newton_raphson(
                function_str, x0, tol, iterations_limit, error_type
            )
            template_data["response"] = response

            approximate_root = response["table"][-1][1]
            plot_a = approximate_root - 1
            plot_b = approximate_root + 1

            template_data["plot_data"] = PlotManager.plot_graph(response, function, plot_a, plot_b)

            return render(request, 'non_linear_equations/newton_raphson.html', {'template_data': template_data})
        else:
            return render(request, 'non_linear_equations/newton_raphson.html', {'template_data': template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(str(e))
        template_data["title"] = "Newton-Raphson Method"
        return render(request, 'non_linear_equations/newton_raphson.html', {'template_data': template_data})

def secant(request):
    template_data = {}
    template_data["title"] = "Secant Method"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Non Linear Equations", reverse("home") + "#methods-section"),
        ("Secant", reverse("methods.secant")),
    ]

    try:
        if request.method == 'POST':
            x0 = float(request.POST.get("x0").replace(',', '.'))
            x1 = float(request.POST.get("x1").replace(',', '.'))
            function_str = request.POST.get("function")
            function = EquationsManager.parse_function(function_str)
            iterations_limit = int(request.POST.get("iterations_limit"))
            error_type = request.POST.get("error_type", "relative")
            tolerance_input = request.POST.get("tolerance").replace(',', '.')
            
            # Convert tolerance_input to tolerance value
            if error_type == 'relative':
                k = int(tolerance_input)
                tolerance = EquationsManager.significant_figures_to_tolerance(k)
            else:
                d = int(tolerance_input)
                tolerance = EquationsManager.correct_decimals_to_tolerance(d)

            response = NonLinearEquationsMethods.secant(
                x0, x1, function, tolerance, iterations_limit, error_type
            )

            template_data["response"] = response

            approximate_root = response["table"][-1][1]

            plot_a = approximate_root - 1
            plot_b = approximate_root + 1

            template_data["plot_data"] = PlotManager.plot_graph(
                response, function, min(plot_a, plot_b), max(plot_a, plot_b)
            )

            return render(request, "non_linear_equations/secant.html", {"template_data": template_data})

        else:
            return render(request, "non_linear_equations/secant.html", {"template_data": template_data})

    except Exception as e:
        template_data["response"] = ResponseManager.error_response(str(e))
        return render(request, "non_linear_equations/secant.html", {"template_data": template_data})


def multiple_roots_v1(request):
    template_data = {}
    template_data["title"] = "Multiple Roots v1"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Non Linear Equations", reverse("home") + "#methods-section"),
        ("Multiple Roots Method v1", reverse("methods.multiple_roots_v1")),
    ]

    try:
        if request.POST:
            function_str = request.POST.get("function")
            function = EquationsManager.parse_function(function_str)
            x0 = float(request.POST.get("x0"))
            multi = float(request.POST.get("multi"))
            tol = float(request.POST.get("tolerance"))
            iterations_limit = int(request.POST.get("iterations_limit"))
            error_type = request.POST.get("error_type", "relative")

            response = NonLinearEquationsMethods.multiple_roots_v1(x0, tol, iterations_limit, multi, function_str)
            template_data["response"] = response

            approximate_root = response["table"][-1][1]

            plot_a = approximate_root - 1
            plot_b = approximate_root + 1

            template_data["plot_data"] = PlotManager.plot_graph(response, function, plot_a, plot_b)
           

            return render(request, 'non_linear_equations/multiple_roots_v1.html', {'template_data': template_data})
        else:
            return render(request, 'non_linear_equations/multiple_roots_v1.html', {'template_data': template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(str(e))
        template_data["title"] = "Método de Raíces Múltiples v1"
        return render(request, 'non_linear_equations/multiple_roots_v1.html', {'template_data': template_data})


def multiple_roots_v2(request):
    template_data = {}
    template_data["title"] = "Multiple Roots v2"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Non Linear Equations", reverse("home") + "#methods-section"),
        ("Multiple Roots Method v2", reverse("methods.multiple_roots_v2")),
    ]

    try:
        if request.POST:
            function_str = request.POST.get("function")
            function = EquationsManager.parse_function(function_str)
            x0 = float(request.POST.get("x0"))
            tol = float(request.POST.get("tolerance"))
            iterations_limit = int(request.POST.get("iterations_limit"))
            error_type = request.POST.get("error_type", "relative")

            response = NonLinearEquationsMethods.multiple_roots_v2(x0, tol, iterations_limit, function_str)
            template_data["response"] = response

            approximate_root = response["table"][-1][1]

            plot_a = approximate_root - 1
            plot_b = approximate_root + 1

            template_data["plot_data"] = PlotManager.plot_graph(response, function, plot_a, plot_b)
            

            return render(request, 'non_linear_equations/multiple_roots_v2.html', {'template_data': template_data})
        else:
            return render(request, 'non_linear_equations/multiple_roots_v2.html', {'template_data': template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(str(e))
        template_data["title"] = "Método Raíces Múltiples v2"
        return render(request, 'non_linear_equations/multiple_roots_v2.html', {'template_data': template_data})
