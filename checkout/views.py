from django.shortcuts import render,\
    redirect, reverse, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

from shop.models import Product
from customers.models import UserAddress
from . models import Order, OrderLine
from . forms import BillingForm, ShippingForm
from cart.contexts import cart_contents


def checkout(request):
    """
    A view to return the checkout page
    """

    if request.POST:
        cart = request.session.get('cart', {})
        shipping_form = ShippingForm(request.POST, prefix="shipping")

        billing_form = BillingForm(request.POST, prefix="billing")

        if shipping_form.is_valid() and billing_form.is_valid():
            # order = billing_form.save(commit=False)

            order = shipping_form.save(commit=False)
            order.save()

            for item_id, quantity in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line = OrderLine(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line.save()

                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart\
                             wasn't found in our database."))
                    order.delete()
                    return redirect(reverse('cart'))
            print(order)
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.id]))
        else:
            messages.error(request, 'There was an error with your form.\
                Please double check your information.')
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "There's nothing\
                 in your cart at the moment")
            return redirect(reverse('shop'))

    if not request.user.is_anonymous:
        address = UserAddress.objects.get(user=request.user)

        form1 = ShippingForm(initial={
            'shipping_name': f'{request.user.first_name} {request.user.last_name}',
            'shipping_address_1': address.address_1,
            'shipping_address_2': address.address_2,
            'shipping_town': address.town,
            'shipping_county': address.county,
            'shipping_postcode': address.postcode,
            'shipping_country': address.country,
        })

        form2 = BillingForm(initial={
            'billing_name': f'{request.user.first_name} {request.user.last_name}',
            'billing_address_1': address.address_1,
            'billing_address_2': address.address_2,
            'billing_town': address.town,
            'billing_county': address.county,
            'billing_postcode': address.postcode,
            'billing_country': address.country,
        })

    else:
        form1 = ShippingForm()
        form2 = BillingForm()

    current_cart = cart_contents(request)
    total = current_cart['grand_total']

    context = {
        'form1': form1,
        'form2': form2,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, id=order_number)

    if request.user.is_authenticated:
        
        profile = UserAddress.objects.get(user=request.user)
        if not order.user_profile == profile:
            order.user_profile = profile  
            order.save()

    if 'cart' in request.session:
        del request.session['cart']
    messages.success(request, f'Order successfully processed! \
        Your order number is {order}.')

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
