from django.shortcuts import render
from methods.utils.MathEquationsManager import MathEquationsManager
from methods.utils.NonLinearEquationsMethods import NonLinearEquationsMethods
from methods.utils.SystemsEquationsMethods import SystemsEquationsMethods

def bisection(request):
    try:
        # a = float(request.a)
        # b = float(request.b)
        # function = MathEquationsManager.parse_function(request.function)
        # tolerance = MathEquationsManager.get_tolerance(request.correct_decimals)
        # iterations_limit = int(request.iterations_limit)

        a = -2
        b = 0
        function = MathEquationsManager.parse_function('3*x + 5')
        tolerance = MathEquationsManager.get_tolerance(2)
        iterations_limit = int(100)

        template_data = NonLinearEquationsMethods.bisection(a, b, function, tolerance, iterations_limit)
    
        return render(request, 'bisection.html', {'template_data': template_data})
    
    except Exception as e:
        template_data = {
            'status': 'error',
            'message': f'An error ocurred: {e}',
        }

        return render(request, 'bisection.html', {'template_data': template_data})
