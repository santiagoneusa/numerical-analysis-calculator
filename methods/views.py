from django.shortcuts import render
from methods.utils.ResponseManager import ResponseManager
from methods.utils.MathEquationsManager import MathEquationsManager
from methods.methods.NonLinearEquationsMethods import NonLinearEquationsMethods
from django.urls import reverse


def bisection(request):
    title = "Bisection method"
    breadcrumbs = [
        ("Home", reverse("home")),
        ("Non Linear Equations", reverse("home") + "#methods-section"),
        ("Bisection", reverse("methods.bisection"))
    ]
    try:
        if request.POST:
            a = float(request.POST.get("a"))
            b = float(request.POST.get("b"))
            function = MathEquationsManager.parse_function(request.POST.get("function"))
            tolerance = float(request.POST.get("correct_decimals"))
            iterations_limit = int(request.POST.get("iterations_limit"))

            template_data = NonLinearEquationsMethods.bisection(
                a, b, function, tolerance, iterations_limit
            )
            template_data["title"] = title
            template_data["breadcrumbs"] = breadcrumbs
            return render(request, "bisection.html", {"template_data": template_data})

        else:
            template_data = ResponseManager.error_response(
                "All the inputs must have a value."
            )
            template_data["title"] = title
            template_data["breadcrumbs"] = breadcrumbs
            return render(request, "bisection.html", {"template_data": template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(e)
        template_data["title"] = title
        template_data["breadcrumbs"] = breadcrumbs
        return render(request, "bisection.html", {"template_data": template_data})

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

def direct_factorization_lu_simple(request):
    pass

def direct_factorization_lu_partial(request):
    pass

def croult(request):
    pass

def doolittle(request):
    pass

def cholesky(request):
    pass

def jacobi(request):
    pass

def gauss_seidel(request):
    pass

def sor(request):
    pass

def vandermonde(request):
    pass

def newton_divided_difference(request):
    pass

def lagrange(request):
    pass

def spline_linear(request):
    pass

def spline_square(request):
    pass

def spline_cubic(request):
    pass