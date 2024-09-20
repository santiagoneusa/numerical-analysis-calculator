from django.urls import path

from . import views

urlpatterns = [
    path("bisection/", views.bisection, name="methods.bisection"),
    path("fixed-point/", views.fixed_point, name="methods.fixed_point"),
    path("false-position/", views.false_position, name="methods.false_position"),
    path("newton-raphson/", views.newton_raphson, name="methods.newton_raphson"),
    path("secant/", views.secant, name="methods.secant"),
    path("multiple-roots-v1/", views.multiple_roots_v1, name="methods.multiple_roots_v1"),
    path("multiple-roots-v2/", views.multiple_roots_v2, name="methods.multiple_roots_v2"),

    path("direct-factorization-lu-simple/", views.direct_factorization_lu_simple, name="methods.direct_factorization_lu_simple"),
    path("direct-factorization-lu-partial/", views.direct_factorization_lu_partial, name="methods.direct_factorization_lu_partial"),
    path("croult/", views.croult, name="methods.croult"),
    path("doolittle/", views.doolittle, name="methods.doolittle"),
    path("cholesky/", views.cholesky, name="methods.cholesky"),
    path("jacobi/", views.jacobi, name="methods.jacobi"),
    path("gauss-seidel/", views.gauss_seidel, name="methods.gauss_seidel"),
    path("sor/", views.sor, name="methods.sor"),
    
    path("vandermonde/", views.vandermonde, name="methods.vandermonde"),
    path("newton-divided-difference/", views.newton_divided_difference, name="methods.newton_divided_difference"),
    path("lagrange/", views.lagrange, name="methods.lagrange"),
    path("spline-linear/", views.spline_linear, name="methods.spline_linear"),
    path("spline-square/", views.spline_square, name="methods.spline_square"),
    path("spline-cubic/", views.spline_cubic, name="methods.spline_cubic"),
]
