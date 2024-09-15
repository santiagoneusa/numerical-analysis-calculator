from django.shortcuts import render

def home(request):
    template_data = {'message': 'Welcome to the calculator app'}
    return render(request, 'home.html', {"template_data": template_data})