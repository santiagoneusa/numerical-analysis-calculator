from django.urls import path
from .views import NonLinearEquationsViews, SystemsEquationsViews, InterpolationViews

urlpatterns = [
    path("bisection", NonLinearEquationsViews.bisection, name="methods.bisection"),
    path(
        "fixed-point", NonLinearEquationsViews.fixed_point, name="methods.fixed_point"
    ),
    path(
        "false-position",
        NonLinearEquationsViews.false_position,
        name="methods.false_position",
    ),
    path(
        "newton-raphson",
        NonLinearEquationsViews.newton_raphson,
        name="methods.newton_raphson",
    ),
    path("secant", NonLinearEquationsViews.secant, name="methods.secant"),
    path(
        "multiple-roots-v1",
        NonLinearEquationsViews.multiple_roots_v1,
        name="methods.multiple_roots_v1",
    ),
    path(
        "multiple-roots-v2",
        NonLinearEquationsViews.multiple_roots_v2,
        name="methods.multiple_roots_v2",
    ),
    path("jacobi", SystemsEquationsViews.jacobi, name="methods.jacobi"),
    path(
        "gauss-seidel", SystemsEquationsViews.gauss_seidel, name="methods.gauss_seidel"
    ),
    path("sor", SystemsEquationsViews.sor, name="methods.sor"),
    path("vandermonde", InterpolationViews.vandermonde, name="methods.vandermonde"),
    path(
        "newton-divided-difference",
        InterpolationViews.newton_divided_difference,
        name="methods.newton_divided_difference",
    ),
    path("lagrange", InterpolationViews.lagrange, name="methods.lagrange"),
    path(
        "spline-linear", InterpolationViews.spline_linear, name="methods.spline_linear"
    ),
]
