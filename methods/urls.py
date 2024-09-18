from django.urls import path

from . import views

urlpatterns = [
    path("bisection/", views.bisection, name="bisection"),
]
