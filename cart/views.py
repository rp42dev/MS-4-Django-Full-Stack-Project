"""
Cart app views
    1. A view to return the cart page
"""
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from shop.models import Product, Category


def cart(request):
    """A view to return the cart page"""
    return render(request, 'cart/cart.html')
