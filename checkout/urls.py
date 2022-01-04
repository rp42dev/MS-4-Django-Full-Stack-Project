"""Checkout App's url's"""
from django.urls import path, include
from . import views
from .webhooks import webhook


urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout/', views.checkout_post, name='checkout_post'),
    path('checkout_success/<order_number>/', views.checkout_success, name='checkout_success'),
    path('wh/', webhook, name='webhook'),
]
