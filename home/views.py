from django.shortcuts import render
from django.urls import reverse


def home(request):
    template_data = {
        "title": "Home",
        "message": "Welcome to the calculator app",
        "breadcrumbs": [("Home", reverse("home"))],
    }
    return render(request, "home.html", {"template_data": template_data})


def about(request):
    template_data = {
        "title": "About",
        "message": "Welcome to the calculator app",
        "breadcrumbs": [("Home", reverse("home")), ("About", reverse("about"))],
    }
    return render(request, "about.html", {"template_data": template_data})


def guide(request):
    template_data = {
        "title": "User Guide",
        "message": "Welcome to the calculator app",
        "breadcrumbs": [("Home", reverse("home")), ("User Guide", reverse("guide"))],
    }
    return render(request, "guide.html", {"template_data": template_data})


def problems(request):
    template_data = {
        "title": "Solutions to Common Problems",
        "message": "Welcome to the calculator app",
        "breadcrumbs": [
            ("Home", reverse("home")),
            ("Solutions to Common Problems", reverse("problems")),
        ],
    }
    return render(request, "problems.html", {"template_data": template_data})
