from django.shortcuts import render


def home(request):
    template_data = {"title": "Home", "message": "Welcome to the calculator app"}
    return render(request, "home.html", {"template_data": template_data})


def about(request):
    template_data = {"title": "About", "message": "Welcome to the calculator app"}
    return render(request, "about.html", {"template_data": template_data})


def guide(request):
    template_data = {"title": "User Guide", "message": "Welcome to the calculator app"}
    return render(request, "guide.html", {"template_data": template_data})


def problems(request):
    template_data = {
        "title": "Solutions to Common Problems",
        "message": "Welcome to the calculator app",
    }
    return render(request, "problems.html", {"template_data": template_data})
