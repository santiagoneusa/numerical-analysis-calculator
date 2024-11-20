from django.shortcuts import render
from methods.utils.ResponseManager import ResponseManager
from methods.utils.MatricesManager import MatricesManager
from methods.methods.SystemsEquationsMethods import SystemsEquationsMethods
from methods.utils.EquationsManager import EquationsManager
from django.urls import reverse


def jacobi(request):
    template_data = {}
    template_data["title"] = "Jacobi method"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Systems of equations", reverse("home") + "#methods-section"),
        ("Jacobi", reverse("methods.jacobi")),
    ]

    try:
        if request.method == 'POST':
            # Obtener las entradas del usuario
            A_string = request.POST.get('A')
            b_string = request.POST.get('b')
            x0_string = request.POST.get('x0')
            Tol = float(request.POST.get('tolerance'))
            niter = int(request.POST.get('iterations_limit'))

            # Convertir las entradas en matrices y vectores NumPy
            A = MatricesManager.parse_matrix(A_string)
            b = MatricesManager.parse_vector(b_string)
            x0 = MatricesManager.parse_vector(x0_string)

            # Validar las entradas
            if not MatricesManager.is_square_matrix(A):
                raise ValueError("The matrix A must be square.")
            if not MatricesManager.are_dimensions_compatible(A, b, x0):
                raise ValueError("The dimensions of A, b and x0 are not compatible.")

            # Llamar al método SOR
            response = SystemsEquationsMethods.jacobi(x0, A, b, Tol, niter)
            template_data.update(response)

            template_data['table_headers'] = ['Iteration', 'x', 'Error']
            return render(request, "systems_equations/jacobi.html", {"template_data": template_data})
        
        else:
            template_data["response"] = ResponseManager.error_response("All the inputs must have a value.")
            return render(request, "systems_equations/jacobi.html", {"template_data": template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(e)
        return render(request, "systems_equations/jacobi.html", {"template_data": template_data})


def gauss_seidel(request):
    template_data = {}
    template_data["title"] = "Gauss-Seidel Method"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Equations systems", reverse("methods.gauss_seidel")),
        ("Gauss-Seidel", reverse("methods.gauss_seidel")),
    ]

    try:
        if request.method == 'POST':
            # Obtener las entradas del usuario
            A_string = request.POST.get('A')
            b_string = request.POST.get('b')
            x0_string = request.POST.get('x0')
            Tol = float(request.POST.get('tolerance'))
            niter = int(request.POST.get('iterations_limit'))

            # Convertir las entradas en matrices y vectores NumPy
            A = MatricesManager.parse_matrix(A_string)
            b = MatricesManager.parse_vector(b_string)
            x0 = MatricesManager.parse_vector(x0_string)

            # Validar las entradas
            if not MatricesManager.is_square_matrix(A):
                raise ValueError("The matrix A must be square.")
            if not MatricesManager.are_dimensions_compatible(A, b, x0):
                raise ValueError("The dimensions of A, b, and x0 are not compatible.")

            # Llamar al método Gauss-Seidel
            response = SystemsEquationsMethods.gauss_seidel(A, b, x0, Tol, niter)
            template_data.update(response)

            # Añadir los encabezados para la tabla
            template_data['table_headers'] = ['Iteration', 'x', 'Error']

            # Renderizar la página con los resultados
            return render(request, "systems_equations/gauss_seidel.html", {"template_data": template_data})

        else:
            # Si el método es GET, solo renderiza el formulario vacío
            return render(request, "systems_equations/gauss_seidel.html", {"template_data": template_data})

    except Exception as e:
        # Si ocurre un error, manejarlo y mostrar el mensaje en la vista
        template_data = ResponseManager.error_response(str(e))
        template_data["title"] = "Gauss-Seidel Method"
        return render(request, "systems_equations/gauss_seidel.html", {"template_data": template_data})


def sor(request):
    template_data = {}
    template_data["title"] = "Method of Successive Over-Relaxation (SOR)"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Equations systems", reverse("methods.sor")),
        ("SOR", reverse("methods.sor")),
    ]

    try:
        if request.method == 'POST':
            # Get user inputs
            A_string = request.POST.get('A')
            b_string = request.POST.get('b')
            x0_string = request.POST.get('x0')
            w = float(request.POST.get('w').replace(',', '.'))
            iterations_limit = int(request.POST.get('iterations_limit'))
            error_type = request.POST.get('error_type', 'relative')
            tolerance_input = request.POST.get('tolerance').replace(',', '.')

            # Convert tolerance_input to tolerance value
            if error_type == 'relative':
                k = int(tolerance_input)
                Tol = EquationsManager.significant_figures_to_tolerance(k)
            else:
                d = int(tolerance_input)
                Tol = EquationsManager.correct_decimals_to_tolerance(d)

            # Convert inputs to NumPy arrays
            A = MatricesManager.parse_matrix(A_string)
            b = MatricesManager.parse_vector(b_string)
            x0 = MatricesManager.parse_vector(x0_string)

            # Validate inputs
            if not MatricesManager.is_square_matrix(A):
                raise ValueError("The matrix A must be square.")
            if not MatricesManager.are_dimensions_compatible(A, b, x0):
                raise ValueError("The dimensions of A, b, and x0 are not compatible.")
            if not (0 < w < 2):
                raise ValueError("The relaxation factor w must be between 0 and 2.")

            # Call the SOR method
            response = SystemsEquationsMethods.sor(x0, A, b, Tol, iterations_limit, w, error_type)
            template_data.update(response)

            template_data['table_headers'] = ['Iteration', 'x', 'Error']
            return render(request, "systems_equations/sor.html", {"template_data": template_data})

        else:
            return render(request, "systems_equations/sor.html", {"template_data": template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(str(e))
        return render(request, "systems_equations/sor.html", {"template_data": template_data})
