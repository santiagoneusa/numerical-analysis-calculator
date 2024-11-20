from django.shortcuts import render
from methods.utils.ResponseManager import ResponseManager
from methods.utils.PlotManager import PlotManager
from methods.methods.InterpolationMethods import InterpolationMethods
from django.urls import reverse


def vandermonde(request):
    template_data = {}
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

    if request.method == 'POST':
        x_values_input = request.POST.get('x_values', '')
        y_values_input = request.POST.get('y_values', '')

        try:
            # Validate that inputs are not empty
            if not x_values_input.strip() or not y_values_input.strip():
                raise ValueError("Both x values and y values must be provided.")

            # Replace commas with spaces and split the inputs
            x_values_str_list = x_values_input.replace(',', ' ').split()
            y_values_str_list = y_values_input.replace(',', ' ').split()

            # Convert the inputs to lists of numbers
            x_values = [float(x) for x in x_values_str_list]
            y_values = [float(y) for y in y_values_str_list]

            # Validate that they have the same length
            if len(x_values) != len(y_values):
                raise ValueError("The vectors x and y must have the same length.")

            # Validate that x_values are in ascending order
            if x_values != sorted(x_values):
                raise ValueError("The x values must be in ascending order.")

            # Validate that x_values are distinct
            if len(set(x_values)) != len(x_values):
                raise ValueError("The x values must be distinct (no duplicates).")

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

        except ValueError as ve:
            # Handle specific value errors
            template_data = ResponseManager.error_response(str(ve))
            template_data["title"] = "Linear Spline Interpolation"
            return render(request, "interpolation/spline_linear.html", {"template_data": template_data})
        except Exception as e:
            # Handle any other exceptions
            template_data = ResponseManager.error_response("An unexpected error occurred: " + str(e))
            template_data["title"] = "Linear Spline Interpolation"
            return render(request, "interpolation/spline_linear.html", {"template_data": template_data})

    else:
        return render(request, "interpolation/spline_linear.html", {"template_data": template_data})


def spline_quadratic(request):
    template_data = {}
    template_data["title"] = "Quadratic Spline Interpolation"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Interpolation", reverse("home") + "#methods-section"),
        ("Quadratic Spline", reverse("methods.spline_quadratic")),
    ]

    if request.method == 'POST':
        x_values_input = request.POST.get('x_values', '')
        y_values_input = request.POST.get('y_values', '')

        try:
            # Validate that inputs are not empty
            if not x_values_input.strip() or not y_values_input.strip():
                raise ValueError("Both x values and y values must be provided.")

            # Replace commas with spaces and split the inputs
            x_values_str_list = x_values_input.replace(',', ' ').split()
            y_values_str_list = y_values_input.replace(',', ' ').split()

            # Convert the inputs to lists of numbers
            x_values = [float(x) for x in x_values_str_list]
            y_values = [float(y) for y in y_values_str_list]

            # Validate that they have the same length
            if len(x_values) != len(y_values):
                raise ValueError("The vectors x and y must have the same length.")

            # Validate that x_values are in ascending order
            if x_values != sorted(x_values):
                raise ValueError("The x values must be in ascending order.")

            # Validate that x_values are distinct
            if len(set(x_values)) != len(x_values):
                raise ValueError("The x values must be distinct (no duplicates).")

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

        except ValueError as ve:
            # Handle specific value errors
            template_data = ResponseManager.error_response(str(ve))
            template_data["title"] = "Quadratic Spline Interpolation"
            return render(request, "interpolation/spline_quadratic.html", {"template_data": template_data})
        except Exception as e:
            # Handle any other exceptions
            template_data = ResponseManager.error_response("An unexpected error occurred: " + str(e))
            template_data["title"] = "Quadratic Spline Interpolation"
            return render(request, "interpolation/spline_quadratic.html", {"template_data": template_data})

    else:
        return render(request, "interpolation/spline_quadratic.html", {"template_data": template_data})

def spline_cubic(request):
    template_data = {}
    template_data["title"] = "Cubic Spline Interpolation"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Interpolation", reverse("home") + "#methods-section"),
        ("Cubic Spline", reverse("methods.spline_cubic")),
    ]

    if request.method == 'POST':
        x_values_input = request.POST.get('x_values', '')
        y_values_input = request.POST.get('y_values', '')

        try:
            # Validate that inputs are not empty
            if not x_values_input.strip() or not y_values_input.strip():
                raise ValueError("Both x values and y values must be provided.")

            # Replace commas with spaces and split the inputs
            x_values_str_list = x_values_input.replace(',', ' ').split()
            y_values_str_list = y_values_input.replace(',', ' ').split()

            # Convert the inputs to lists of numbers
            x_values = [float(x) for x in x_values_str_list]
            y_values = [float(y) for y in y_values_str_list]

            # Validate that they have the same length
            if len(x_values) != len(y_values):
                raise ValueError("The vectors x and y must have the same length.")

            # Validate that x_values are in ascending order
            if x_values != sorted(x_values):
                raise ValueError("The x values must be in ascending order.")

            # Validate that x_values are distinct
            if len(set(x_values)) != len(x_values):
                raise ValueError("The x values must be distinct (no duplicates).")

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

        except ValueError as ve:
            # Handle specific value errors
            template_data = ResponseManager.error_response(str(ve))
            template_data["title"] = "Cubic Spline Interpolation"
            return render(request, "interpolation/spline_cubic.html", {"template_data": template_data})
        except Exception as e:
            # Handle any other exceptions
            template_data = ResponseManager.error_response("An unexpected error occurred: " + str(e))
            template_data["title"] = "Cubic Spline Interpolation"
            return render(request, "interpolation/spline_cubic.html", {"template_data": template_data})

    else:
        return render(request, "interpolation/spline_cubic.html", {"template_data": template_data})
