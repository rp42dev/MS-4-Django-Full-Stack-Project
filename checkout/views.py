from django.shortcuts import render,\
    redirect, reverse, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

from shop.models import Product
from customers.models import UserAddress
from . models import Order, OrderLine
from . forms import OrderForm
from cart.contexts import cart_contents


import json

def checkout(request):
    """
    A view to return the checkout page
    """
    
    if request.POST:
        cart = request.session.get('cart', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'address_line_1': request.POST['address_line_1'],
            'address_line_2': request.POST['address_line_2'],
            'town': request.POST['town'],
            'postcode': request.POST['postcode'],
            'county': request.POST['county'],
            'country': request.POST['country'],
        }
        form = OrderForm(form_data)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            for item_id, quantity in cart.items():
                try:
                    item = Product.objects.get(id=item_id)
                    order_line = OrderLine(
                        order=order,
                        item=item,
                        quantity=quantity,
                    )
                    order_line.save()
                    profile = UserAddress.objects.get(user=request.user)
                    order.user = profile
                    order.status = 'PSH'
                    print(order.status)
                    order.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found in our database."))
                    order.delete()
                    return redirect(reverse('cart'))
            request.session['save_info'] = 'save-info' in request.POST
            
            if 'cart' in request.session:
                del request.session['cart']
            messages.success(request, 'all good')
            return redirect(reverse('shop'))
        else:
            messages.error(request, 'There was an error with your form.\
                Please double check your information.')
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "There's nothing in your cart at the moment")
            return redirect(reverse('shop'))

    if not request.user.is_anonymous:
        address = UserAddress.objects.get(user=request.user)
        form = OrderForm(initial={
            'full_name': f'{request.user.first_name} {request.user.last_name}',
            'email': request.user.email,
            'address_line_1': address.address_line_1,
            'address_line_2': address.address_line_2,
            'town': address.town,
            'postcode': address.postcode,
            'county': address.county,
            'country': address.country,
        })
    else:  
        form = OrderForm()
   
    current_cart = cart_contents(request)
    total = current_cart['grand_total']
    context={
        'form': form,
    }

    return render(request, 'checkout/checkout.html', context)
