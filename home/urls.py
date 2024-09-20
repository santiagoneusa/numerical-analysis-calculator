from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("guide/", views.guide, name="guide"),
    path("problems/", views.problems, name="problems"),
]
