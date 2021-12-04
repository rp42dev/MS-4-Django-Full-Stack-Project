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
    update = product.item_count - quantity
    # product.item_count = 10
    # product.save()

    if update < 0:
        messages.error(
            request, f'Sorry, only {product.item_count} \
                {product.name} available')
        return redirect(redirect_url)
    else:
        product.item_count = update
        product.save()

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity

    request.session['cart'] = cart
    messages.success(
            request, f'{quantity} \
                {product.name} added to the cart!')

    return redirect(redirect_url)


def update_cart(request, item_id):
    """update the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    action = request.POST.get('action')
    cart = request.session.get('cart', {})

    if action == 'minus':
        if cart[item_id] == 1:
            cart.pop(item_id)
            product.item_count += 1
            product.save()
            messages.success(
                request, f'Removed {product.name}\
                    from your bag')
        else:
            cart[item_id] -= 1
            product.item_count += 1
            product.save()
            messages.success(
                request, f'The hat {product.name}\
                     quantity was updated to {cart[item_id]}')
    elif action == 'add':
        if product.item_count != 0:
            cart[item_id] += 1
            product.item_count -= 1
            product.save()
            messages.success(
                request, f'The hat {product.name}\
                     quantity was updated to {cart[item_id]}')
        else:
            messages.error(
                request, f'Sorry, the {product.name}\
                    hat is currently out of stock')

    request.session['cart'] = cart
    return redirect(reverse('cart'))
