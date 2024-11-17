from django.shortcuts import render
from methods.utils.ResponseManager import ResponseManager
from methods.utils.MatricesManager import MatricesManager
from methods.methods.SystemsEquationsMethods import SystemsEquationsMethods
from django.urls import reverse


def jacobi(request):
    template_data["title"] = "Jacobi method"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Systems of equations", reverse("home") + "#methods-section"),
        ("Jacobi", reverse("methods.jacobi")),
    ]

    try:
        if request.POST:
            # TODO: Get the inputs
            # TODO: Implement Jacobi method
            # TODO: Implement the response
            return render(request, "systems_equations/jacobi.html", {"template_data": template_data})
        else:
            template_data["response"] = ResponseManager.error_response("All the inputs must have a value.")
            return render(request, "systems_equations/jacobi.html", {"template_data": template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(e)
        return render(request, "systems_equations/jacobi.html", {"template_data": template_data})


def gauss_seidel(request):
    template_data["title"] = "Gauss-Seidel method"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Systems of equations", reverse("home") + "#methods-section"),
        ("Gauss-Seidel", reverse("methods.gauss_seidel")),
    ]

    try:
        if request.POST:
            # TODO: Get the inputs
            # TODO: Implement Gauss-Seidel method
            # TODO: Implement the response
            return render(request, "systems_equations/gauss_seidel.html", {"template_data": template_data})
        else:
            template_data["response"] = ResponseManager.error_response("All the inputs must have a value.")
            return render(request, "systems_equations/gauss_seidel.html", {"template_data": template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(e)
        return render(request, "systems_equations/gauss_seidel.html", {"template_data": template_data})


def sor(request):
    template_data["title"] = "Successive over-relaxation method"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Systems of equations", reverse("home") + "#methods-section"),
        ("Successive over-relaxation", reverse("methods.sor")),
    ]

    try:
        if request.POST:
            # TODO: Get the inputs
            # TODO: Implement Successive over-relaxation method
            # TODO: Implement the response
            return render(request, "systems_equations/sor.html", {"template_data": template_data})
        else:
            template_data["response"] = ResponseManager.error_response("All the inputs must have a value.")
            return render(request, "systems_equations/sor.html", {"template_data": template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(e)
        return render(request, "systems_equations/sor.html", {"template_data": template_data})
