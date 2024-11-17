from django.shortcuts import render
from methods.utils.ResponseManager import ResponseManager
from methods.utils.EquationsManager import EquationsManager
from methods.methods.InterpolationMethods import InterpolationMethods
from django.urls import reverse


def vandermonde(request):
    template_data["title"] = "Vandermonde method"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Interpolation", reverse("home") + "#methods-section"),
        ("Vandermonde", reverse("methods.vandermonde")),
    ]

    try:
        if request.POST:
            # TODO: Get the inputs
            # TODO: Implement Vandermonde method
            # TODO: Implement the response
            return render(request, "interpolation/vandermonde.html", {"template_data": template_data})
        else:
            template_data["response"] = ResponseManager.error_response("All the inputs must have a value.")
            return render(request, "interpolation/vandermonde.html", {"template_data": template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(e)
        return render(request, "interpolation/vandermonde.html", {"template_data": template_data})


def newton_divided_difference(request):
    template_data["title"] = "Newton divided difference method"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Interpolation", reverse("home") + "#methods-section"),
        ("Newton divided difference", reverse("methods.newton_divided_difference")),
    ]

    try:
        if request.POST:
            # TODO: Get the inputs
            # TODO: Implement Newton divided difference method
            # TODO: Implement the response
            return render(request, "interpolation/newton_divided_difference.html", {"template_data": template_data})
        else:
            template_data["response"] = ResponseManager.error_response("All the inputs must have a value.")
            return render(request, "interpolation/newton_divided_difference.html", {"template_data": template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(e)
        return render(request, "interpolation/newton_divided_difference.html", {"template_data": template_data})


def lagrange(request):
    template_data["title"] = "Lagrange method"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Interpolation", reverse("home") + "#methods-section"),
        ("Lagrange", reverse("methods.lagrange")),
    ]

    try:
        if request.POST:
            # TODO: Get the inputs
            # TODO: Implement Lagrange method
            # TODO: Implement the response
            return render(request, "interpolation/lagrange.html", {"template_data": template_data})
        else:
            template_data["response"] = ResponseManager.error_response("All the inputs must have a value.")
            return render(request, "interpolation/lagrange.html", {"template_data": template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(e)
        return render(request, "interpolation/lagrange.html", {"template_data": template_data})


def spline_linear(request):
    template_data["title"] = "Spline linear method"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Interpolation", reverse("home") + "#methods-section"),
        ("Spline linear", reverse("methods.spline_linear")),
    ]

    try:
        if request.POST:
            # TODO: Get the inputs
            # TODO: Implement Spline linear method
            # TODO: Implement the response
            return render(request, "interpolation/spline_linear.html", {"template_data": template_data})
        else:
            template_data["response"] = ResponseManager.error_response("All the inputs must have a value.")
            return render(request, "interpolation/spline_linear.html", {"template_data": template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(e)
        return render(request, "interpolation/spline_linear.html", {"template_data": template_data})
