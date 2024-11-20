from django.shortcuts import render
from methods.utils.ResponseManager import ResponseManager
from methods.utils.MatricesManager import MatricesManager
from methods.methods.SystemsEquationsMethods import SystemsEquationsMethods
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
    template_data = {}
    template_data["title"] = "Method of Successive Over-Relaxation (SOR)"
    template_data["breadcrumbs"] = [
        ("Home", reverse("home")),
        ("Equations systems", reverse("methods.sor")),
        ("SOR", reverse("methods.sor")),
    ]

    try:
        if request.method == 'POST':
            # Obtener las entradas del usuario
            A_string = request.POST.get('A')
            b_string = request.POST.get('b')
            x0_string = request.POST.get('x0')
            Tol = float(request.POST.get('tolerance'))
            niter = int(request.POST.get('iterations_limit'))
            w = float(request.POST.get('w'))

            # Convertir las entradas en matrices y vectores NumPy
            A = MatricesManager.parse_matrix(A_string)
            b = MatricesManager.parse_vector(b_string)
            x0 = MatricesManager.parse_vector(x0_string)

            # Validar las entradas
            if not MatricesManager.is_square_matrix(A):
                raise ValueError("The matrix A must be square.")
            if not MatricesManager.are_dimensions_compatible(A, b, x0):
                raise ValueError("The dimensions of A, b and x0 are not compatible.")
            if not (0 < w < 2):
                raise ValueError("The relaxation factor w must be between 0 and 2.")

            # Llamar al método SOR
            response = SystemsEquationsMethods.sor(x0, A, b, Tol, niter, w)
            template_data.update(response)

            template_data['table_headers'] = ['Iteration', 'x', 'Error']
            return render(request, "systems_equations/sor.html", {"template_data": template_data})

        else:
            return render(request, "systems_equations/sor.html", {"template_data": template_data})

    except Exception as e:
        template_data = ResponseManager.error_response(str(e))
        template_data["title"] = "Method of Successive Over-Relaxation (SOR)"
        return render(request, "systems_equations/sor.html", {"template_data": template_data})
