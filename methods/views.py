from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    template_data = {'message': 'Welcome to the calculator app'}
    return render(request, 'home/index.html', {"template_data": template_data})