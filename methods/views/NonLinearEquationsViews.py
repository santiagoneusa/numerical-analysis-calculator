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
    pass


def false_position(request):
    pass


def newton_raphson(request):
    template_data = {}
    template_data["title"] = "Newton-Raphson Method"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Non Linear Equations", reverse("home") + "#methods-section"),
        ("Newton-Raphson", reverse("methods.newton_raphson")),
    ]

    try:
        if request.POST:
            function_str = request.POST.get("function")
            function = EquationsManager.parse_function(function_str)
            x0 = float(request.POST.get("x0"))
            tol = float(request.POST.get("tolerance"))
            iterations_limit = int(request.POST.get("iterations_limit"))
            error_type = request.POST.get("error_type", "relative")

            response = NonLinearEquationsMethods.newton_raphson(function_str, x0, tol, iterations_limit, error_type)
            template_data["response"] = response

            approximate_root = response["table"][-1][1]

            plot_a = approximate_root - 1
            plot_b = approximate_root + 1

            template_data["plot_data"] = PlotManager.plot_graph(response, function, plot_a, plot_b)
            print(f"Plot data: {template_data['plot_data']}")

            return render(request, 'non_linear_equations/newton_raphson.html', {'template_data': template_data})
        else:
            return render(request, 'non_linear_equations/newton_raphson.html', {'template_data': template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(str(e))
        template_data["title"] = "Método de Newton-Raphson"
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
        if request.POST:
            x0 = float(request.POST.get("x0"))
            x1 = float(request.POST.get("x1"))
            function_str = request.POST.get("function")
            function = EquationsManager.parse_function(function_str)
            tolerance = float(request.POST.get("correct_decimals"))
            iterations_limit = int(request.POST.get("iterations_limit"))

            response = NonLinearEquationsMethods.secant(x0, x1, function, tolerance, iterations_limit)

            template_data["response"] = response

            approximate_root = response["table"][-1][1]

            plot_a = approximate_root - 1
            plot_b = approximate_root + 1
            
            template_data["plot_data"] = PlotManager.plot_graph(response, function, min(plot_a, plot_b), max(plot_a, plot_b))

            return render(request, "non_linear_equations/secant.html", {"template_data": template_data})

        else:
            template_data["response"] = ResponseManager.error_response("All inputs must have a value.")
            return render(request, "non_linear_equations/secant.html", {"template_data": template_data})

    except Exception as e:
        template_data["response"] = ResponseManager.error_response(str(e))
        return render(request, "non_linear_equations/secant.html", {"template_data": template_data})


def multiple_roots_v1(request):
    pass


def multiple_roots_v2(request):
    pass
