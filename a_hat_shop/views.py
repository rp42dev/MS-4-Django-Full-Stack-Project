"""
https://stackoverflow.com/questions/48636054/
how-do-i-redirect-errors-like-404-or-500-or-403-to-a-custom-error-page-in-apache
"""
from django.shortcuts import render


def error_500(request):
    """
    Handle internal server errors
    """
    contexts = {}
    return render(request, 'errors/500.html', contexts)


def error_404(request, exception):
    """
    Handle page not found errors
    """
    context = {}
    return render(request, "errors/404.html", context)


def error_403(request, exception):
    """
    Handle bad request errors
    """
    contexts = {}
    return render(request, 'errors/403.html', contexts)


def error_400(request,  exception):
    """
    Handle client side errors
    """
    contexts = {}
    return render(request, 'errors/400.html', contexts)


def csrf_failure(request, reason=""):
    """
    Handle csfr token failures
    https://stackoverflow.com/questions/40758711/
    how-to-set-a-default-handler-for-csrf-verification-failed-in-django
    """
    contexts = {}
    return render(request, 'errors/403_csfr.html', contexts)
