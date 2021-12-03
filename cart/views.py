"""
Cart app views
    1. A view to return the cart page
Add to cart
    1. Add items to the shopping cart
"""
from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from shop.models import Product, Category


def cart(request):
    """A view to return the cart page"""
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """ Add items to the shopping cart """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})
    print(item_id)

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity

    request.session['cart'] = cart

    return redirect(redirect_url)
