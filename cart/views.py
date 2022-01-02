"""
Cart app views
    1. A view to return the cart page
Add to cart
    1. Add items to the shopping cart
     Check if items are available in stock
    3. Update Cart quantity of the product
    4. delete item specified from the cart
"""
from django.shortcuts import render, redirect,\
    reverse, HttpResponse, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from shop.models import Product, Category


def cart_view(request):
    """
    A view to return the cart page
    Check if items are available in stock
    before returning cart page view
    if product availability changed
    adjust product count to availablility
    if product count is 0 remove product
    from the cart altogether
    """
    cart = request.session.get('cart', {})
    url_back = HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if not cart:
        messages.warning(
                    request, 'Your cart is empty.')
        if url_back is not None:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect(reverse('shop'))
    else:

        for key in cart.copy():
            product = get_object_or_404(Product, pk=key)
            if product.item_count < cart[key]:
                if product.item_count <= 0:
                    cart.pop(key)
                    request.session.modified = True
                    messages.warning(request, f'The product {product.name}\
                        has been removed from cart because it is out of stock')
                else:
                    cart[key] = product.item_count
                    request.session.modified = True
                    messages.warning(
                        request, f'The product {product.name} availability\
                            has changed to {product.item_count} in stock:')

        return render(request, 'cart/cart.html')


@require_POST
def add_to_cart(request, item_id):
    """ 
    Add items to the shopping cart
    calculate stock vs cart product
    availability and restrict sellecting
    products to actual stock availability
    """
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    stock = product.item_count - quantity

    if item_id in list(cart.keys()):
        stock_cart = stock - cart[item_id]
        if stock_cart < 0:
            messages.warning(
                    request, f'Only {product.item_count}\
                        {product.name} was in stock items.')
            return redirect(redirect_url)
        else:
            cart[item_id] += quantity
    else:
        if stock < 0:
            messages.warning(
                request, f'Only {product.item_count}\
                    {product.name} was in stock items.')
            return redirect(redirect_url)

        else:
            cart[item_id] = quantity

    request.session['cart'] = cart
    messages.success(
            request, f'{quantity} \
                {product.name} added to the cart!')

    return redirect(redirect_url)


@require_POST
def update_cart(request, item_id):
    """
    update the quantity of the specified
    product to the specified amount
    calculate stock vs cart product
    availability and restrict sellecting
    products to actual stock availability
    """
    product = get_object_or_404(Product, pk=item_id)
    cart = request.session.get('cart', {})

    if request.POST and cart:
        action = request.POST.get('action')

        if action == 'minus':
            if cart[item_id] == 1:
                cart.pop(item_id)
                request.session.modified = True
                messages.success(
                    request, f'Removed {product.name}\
                        from your bag.')
            else:
                cart[item_id] -= 1

                messages.success(
                    request, f'The hat {product.name}\
                            quantity was updated to {cart[item_id]}.')
        elif action == 'add':
            if product.item_count - cart[item_id] <= 0:
                cart[item_id] = product.item_count
                messages.warning(
                    request, f'Only {product.item_count}\
                         {product.name} available.')
            else:
                cart[item_id] += 1
                messages.success(
                    request, f'The hat {product.name}\
                            quantity was updated to {cart[item_id]}.')

    request.session['cart'] = cart

    if cart:
        return redirect(reverse('cart'))
    else:
        messages.warning(
                    request, 'Your cart is empty.')
        return redirect(reverse('shop'))


@require_POST
def remove_cart_item(request, item_id):
    """
    delete item specified from the cart
    chect if there is items in the cart
    and return cart views if there is items
    left in the cart, othervise return to shop
    """
    product = get_object_or_404(Product, pk=item_id)
    cart = request.session.get('cart', {})
    cart.pop(item_id)
    request.session.modified = True
    messages.success(
                    request, f'The hat {product.name}\
                            was removed from cart')
    if cart:
        return redirect(reverse('cart'))
    else:
        messages.info(
                    request, 'Your cart is empty.')
        return redirect(reverse('shop'))
