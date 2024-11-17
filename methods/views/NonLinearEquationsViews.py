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
            a = float(request.POST.get("a"))
            b = float(request.POST.get("b"))
            function_str = request.POST.get("function")
            function = EquationsManager.parse_function(function_str)
            tolerance = float(request.POST.get("correct_decimals"))
            iterations_limit = int(request.POST.get("iterations_limit"))

            response = NonLinearEquationsMethods.bisection(a, b, function, tolerance, iterations_limit)
            template_data["response"] = response
            template_data["plot_data"] = PlotManager.plot_graph(response, function, a, b)

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
    pass


def secant(request):
    pass


def multiple_roots_v1(request):
    pass


def multiple_roots_v2(request):
    pass
