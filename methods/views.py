from django.shortcuts import render
from methods.utils.MathEquationsManager import MathEquationsManager
from methods.methods.NonLinearEquationsMethods import NonLinearEquationsMethods

def bisection(request):
    title = 'Bisection method'
    try:
        if request.POST:
            a = float(request.POST.get('a'))
            b = float(request.POST.get('b'))
            function = MathEquationsManager.parse_function(request.POST.get('function'))
            tolerance = MathEquationsManager.get_tolerance(int(request.POST.get('correct_decimals')))
            iterations_limit = int(request.POST.get('iterations_limit'))

            template_data = NonLinearEquationsMethods.bisection(a, b, function, tolerance, iterations_limit)
            template_data['title'] = title
            
            return render(request, 'bisection.html', {'template_data': template_data})
        
        else:
            # change this to ResponseManager.error_response('All the inputs must have a value.')
            template_data = {
                'title': title,
                'status': 'error',
                'message': 'All the inputs must have a value.',
            }
            return render(request, 'bisection.html', {'template_data': template_data})
        
    except Exception as e:
        # change this to ResponseManager.error_response(e)
        template_data = {
            'title': title,
            'status': 'error',
            'message': f'An error ocurred: {e}.',
        }
        return render(request, 'bisection.html', {'template_data': template_data})
