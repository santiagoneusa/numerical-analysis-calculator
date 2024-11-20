from django.shortcuts import render
from methods.utils.ResponseManager import ResponseManager
from methods.utils.PlotManager import PlotManager
from methods.methods.InterpolationMethods import InterpolationMethods
from django.urls import reverse


def vandermonde(request):
    template_data = {}
    template_data["title"] = "Vandermonde Method"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Interpolation", reverse("home") + "#methods-section"),
        ("Vandermonde", reverse("methods.vandermonde")),
    ]

    try:
        if request.method == 'POST':
            x_values = request.POST.get('x_values')
            y_values = request.POST.get('y_values')

            # Convert the inputs to lists of numbers
            x_values = list(map(float, x_values.strip().split()))
            y_values = list(map(float, y_values.strip().split()))

            # Validate that they have the same length
            if len(x_values) != len(y_values):
                raise ValueError("The vectors x and y must have the same length.")

            # Call the Vandermonde method to compute the matrix and polynomial
            response = InterpolationMethods.vandermonde(x_values, y_values)

            # Debugging lines (to check the output in the terminal)
            print("First row of Vandermonde Matrix:", response['matrix'][1])
            print("First coefficient of Polynomial:", response['coefficients'][1])
            
            # Add matrix, polynomial, and coefficients to the template context
            template_data["matrix"] = response['matrix']
            template_data["polynomial"] = response['polynomial']
            template_data["coefficients"] = response['coefficients']

            # Prepare table data for displaying coefficients, if needed
            table = []
            for i, coeff in enumerate(response['coefficients']):
                table.append([f"x^{i}", f"{coeff:.4f}"])

            # Add table data and headers for rendering in the template
            template_data["table"] = table
            template_data["headers"] = ['Term', 'Coefficient']

            print("Template data:", template_data)  # Debugging line

            return render(request, "interpolation/vandermonde.html", {"template_data": template_data})

        else:
            template_data["response"] = ResponseManager.error_response("All the inputs must have a value.")
            return render(request, "interpolation/vandermonde.html", {"template_data": template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(str(e))
        return render(request, "interpolation/vandermonde.html", {"template_data": template_data})


def newton_divided_difference(request):
    template_data = {}
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
    template_data = {}
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
    template_data = {}
    template_data["title"] = "Linear Spline Interpolation"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Interpolation", reverse("home") + "#methods-section"),
        ("Linear Spline", reverse("methods.spline_linear")),
    ]

    try:
        if request.method == 'POST':
            x_values = request.POST.get('x_values')
            y_values = request.POST.get('y_values')

            # Convert the inputs to lists of numbers
            x_values = list(map(float, x_values.strip().split()))
            y_values = list(map(float, y_values.strip().split()))

            # Validate that they have the same length
            if len(x_values) != len(y_values):
                raise ValueError("The vectors x and y must have the same length.")

            # Call the linear spline method
            response = InterpolationMethods.spline_linear(x_values, y_values)

            # Generate the graphic
            graphic = PlotManager.plot_linear_spline(
                x=response['plot_data']['x'],
                y=response['plot_data']['y'],
                coefficients=response['plot_data']['coefficients']
            )

            # Add the graphic to the template_data
            response['graphic'] = graphic

            template_data.update(response)
            return render(request, "interpolation/spline_linear.html", {"template_data": template_data})

        else:
            return render(request, "interpolation/spline_linear.html", {"template_data": template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(str(e))
        template_data["title"] = "Linear Spline Interpolation"
        return render(request, "interpolation/spline_linear.html", {"template_data": template_data})


def spline_quadratic(request):
    template_data = {}
    template_data["title"] = "Quadratic Spline Interpolation"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Interpolation", reverse("home") + "#methods-section"),
        ("Quadratic Spline", reverse("methods.spline_quadratic")),
    ]

    try:
        if request.method == 'POST':
            x_values = request.POST.get('x_values')
            y_values = request.POST.get('y_values')

            # Convert the inputs to lists of numbers
            x_values = list(map(float, x_values.strip().split()))
            y_values = list(map(float, y_values.strip().split()))

            # Validate that they have the same length
            if len(x_values) != len(y_values):
                raise ValueError("The vectors x and y must have the same length.")

            # Call the quadratic spline method
            response = InterpolationMethods.spline_quadratic(x_values, y_values)

            # Generate the graphic
            graphic = PlotManager.plot_quadratic_spline(
                x=response['plot_data']['x'],
                y=response['plot_data']['y'],
                coefficients=response['plot_data']['coefficients']
            )

            # Add the graphic to the response
            response['graphic'] = graphic

            template_data.update(response)
            return render(request, "interpolation/spline_quadratic.html", {"template_data": template_data})

        else:
            return render(request, "interpolation/spline_quadratic.html", {"template_data": template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(str(e))
        template_data["title"] = "Quadratic Spline Interpolation"
        return render(request, "interpolation/spline_quadratic.html", {"template_data": template_data})

def spline_cubic(request):
    template_data = {}
    template_data["title"] = "Cubic Spline Interpolation"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Interpolation", reverse("home") + "#methods-section"),
        ("Cubic Spline", reverse("methods.spline_cubic")),
    ]

    try:
        if request.method == 'POST':
            x_values = request.POST.get('x_values')
            y_values = request.POST.get('y_values')

            # Convert the inputs to lists of numbers
            x_values = list(map(float, x_values.strip().split()))
            y_values = list(map(float, y_values.strip().split()))

            # Validate that they have the same length
            if len(x_values) != len(y_values):
                raise ValueError("The vectors x and y must have the same length.")

            # Call the cubic spline method
            response = InterpolationMethods.spline_cubic(x_values, y_values)

            # Generate the graphic
            graphic = PlotManager.plot_cubic_spline(
                x=response['plot_data']['x'],
                y=response['plot_data']['y'],
                coefficients=response['plot_data']['coefficients']
            )

            # Add the graphic to the response
            response['graphic'] = graphic

            template_data.update(response)
            return render(request, "interpolation/spline_cubic.html", {"template_data": template_data})

        else:
            return render(request, "interpolation/spline_cubic.html", {"template_data": template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(str(e))
        template_data["title"] = "Cubic Spline Interpolation"
        return render(request, "interpolation/spline_cubic.html", {"template_data": template_data})