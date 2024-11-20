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

            return render(request, "interpolation/vandermonde.html", template_data)


        else:
            template_data["response"] = ResponseManager.error_response("All the inputs must have a value.")
            return render(request, "interpolation/vandermonde.html", template_data)


    except Exception as e:
        template_data = ResponseManager.error_response(str(e))
        return render(request, "interpolation/vandermonde.html", template_data)



def newton_divided_difference(request):
    template_data = {}
    template_data["title"] = "Newton Divided Difference Method"

    try:
        if request.method == 'POST':
            # Obtener los valores de entrada del formulario
            x_values_input = request.POST.get('x_values', '')
            y_values_input = request.POST.get('y_values', '')

            # Validar que se ingresen ambos valores
            if not x_values_input.strip() or not y_values_input.strip():
                raise ValueError("Both x values and y values must be provided.")

            # Convertir las entradas a listas de números
            x_values = list(map(float, x_values_input.replace(',', ' ').split()))
            y_values = list(map(float, y_values_input.replace(',', ' ').split()))
            x_to_interpolate_input = request.POST.get('x_to_interpolate', '').strip()
            if not x_to_interpolate_input:
                raise ValueError("You must provide a value for x to interpolate.")

            x_to_interpolate = float(x_to_interpolate_input)



            # Validar que los vectores x y y tengan la misma longitud
            if len(x_values) != len(y_values):
                raise ValueError("The x and y vectors must have the same length.")

            # Validar que los valores de x sean únicos
            if len(set(x_values)) != len(x_values):
                raise ValueError("The x values must be distinct (no duplicates).")

            # Llamar al método de interpolación de Newton Divided Difference
            response = InterpolationMethods.newton_divided_difference(x_values, y_values, x_to_interpolate)

            # Generar el gráfico
            graphic = PlotManager.plot_newton_divided_difference(response['plot_data']['x'], response['plot_data']['y'])

            # Agregar el gráfico y otros datos a la plantilla
            response['graphic'] = graphic
            template_data.update(response)

            # Renderizar la plantilla con los datos generados
            return render(request, "interpolation/newton_divided_difference.html", {"template_data": template_data})

        else:
            # Si es un GET, solo renderizamos la plantilla vacía
            return render(request, "interpolation/newton_divided_difference.html", {"template_data": template_data})

    except Exception as e:
        # Si hay un error, capturarlo y renderizarlo en la plantilla
        template_data = ResponseManager.error_response(str(e))
        template_data["title"] = "Newton Divided Difference Method"
        return render(request, "interpolation/newton_divided_difference.html", {"template_data": template_data})


def lagrange(request):
    template_data = {}
    template_data["title"] = "Lagrange Interpolation"

    try:
        if request.method == 'POST':
            # Obtener los valores de entrada del formulario
            x_values = request.POST.get('x_values')
            y_values = request.POST.get('y_values')
            x_to_interpolate = float(request.POST.get('x'))

            # Convertir las entradas a listas de números
            x_values = list(map(float, x_values.strip().split()))
            y_values = list(map(float, y_values.strip().split()))

            # Validar que los vectores x y y tengan la misma longitud
            if len(x_values) != len(y_values):
                raise ValueError("Los vectores x e y deben tener la misma longitud.")

            # Llamar al método de interpolación de Lagrange
            response = InterpolationMethods.lagrange(x_values, y_values, x_to_interpolate)

            # Generar el gráfico (si es necesario)
            graphic = PlotManager.plot_newton_divided_difference(
                x=response['plot_data']['x'],
                y=response['plot_data']['y']
            )

            # Agregar el gráfico a los datos de la plantilla
            response['graphic'] = graphic

            # Añadir la respuesta de la interpolación y el gráfico a los datos de la plantilla
            template_data.update(response)

            # Renderizar la plantilla con los datos generados
            return render(request, "interpolation/lagrange.html", {"template_data": template_data})

        else:
            # Si es un GET, solo renderizamos la plantilla vacía
            return render(request, "interpolation/lagrange.html", {"template_data": template_data})

    except Exception as e:
        # Si hay un error, capturarlo y renderizarlo en la plantilla
        template_data = ResponseManager.error_response(str(e))
        template_data["title"] = "Lagrange Interpolation"
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
