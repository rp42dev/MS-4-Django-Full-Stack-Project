"""
Checkout
    1. A view to return the checkout page
Post Checkut
    2. A view to return the checkout post functionality
     Check if items are available in stock
    3. Update Cart quantity of the product
    4. delete item specified from the cart
"""

from django.shortcuts import render,\
    redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings

from cart.contexts import cart_contents
from shop.models import Product
from customers.models import UserAddress
from . models import Order, OrderLine
from . forms import ShippingForm, ContactForm

import stripe
import json


def checkout(request):
    """
    A view to return the checkout page
    Check item stock availability
    Create Stripe Payment intent
    Add checkout forms to the context
    If user authentuicated prefill
    forms with saved shipping form data
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, "There's nothing\
                in your cart at the moment")
        return redirect(reverse('shop'))

    current_cart = cart_contents(request)
    total = current_cart['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
        metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'username': request.user,
        }
    )

    for item_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=item_id)
            stock = product.item_count - quantity
            if product.item_count <= 0:
                messages.error(request, (
                    f"The {product.name} in your cart\
                        stock quantity changed. Curently out of stock"))
                order.delete()
                return redirect(reverse('cart'))
            elif stock < 0:
                messages.error(request, (
                    f"The {product.name} in your cart\
                        stock quantity changed. Curently\
                        {product.item_count} available"))
                order.delete()
                return redirect(reverse('cart'))

        except Product.DoesNotExist:
            messages.error(request, (
                "One of the products in your cart\
                        wasn't found in our database."))
            order.delete()
            return redirect(reverse('cart'))

    if request.user.is_authenticated:
        form2 = ContactForm()
        profile = request.user
        form2 = ContactForm(initial={
            'full_name': f'{profile.first_name} {profile.last_name}',
            'email': profile.email,
        })

        try:
            address = UserAddress.objects.get(user=profile)
            form = ShippingForm(initial={
                'shipping_name': f'{profile.first_name} {profile.last_name}',
                'address_line_1': address.address_line_1,
                'address_line_2': address.address_line_2,
                'city': address.city,
                'county': address.county,
                'postcode': address.postcode,
                'country': address.country,
            })

        except UserAddress.DoesNotExist:
            form = ShippingForm()
            form2 = ContactForm()
    else:
        form = ShippingForm()
        form2 = ContactForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    context = {
        'form2': form2,
        'form': form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)


@require_POST
def checkout_post(request):
    """
    A view to return the checkout post functionality
    Chect stock availability and reduce stock on POST
    Request form data and submit order to database
    """
    cart = request.session.get('cart', {})
    shipping_form = ShippingForm(request.POST, prefix="shipping")
    contact_form = ContactForm(request.POST, prefix="contact")

    if shipping_form.is_valid() and contact_form.is_valid():
        order = shipping_form.save(commit=False)
        pid = request.POST.get('client_secret').split('_secret')[0]
        order.stripe_pid = pid
        order.items = json.dumps(cart)
        order.full_name = request.POST.get('contact-full_name')
        order.email = request.POST.get('contact-email')
        order.save()

        for item_id, quantity in cart.items():
            try:
                product = Product.objects.get(id=item_id)
                stock = product.item_count - quantity
                if product.item_count <= 0:
                    messages.error(request, (
                        f"The {product.name} in your cart\
                            stock quantity changed. Curently out of stock"))
                    order.delete()
                    return redirect(reverse('cart'))
        
                elif stock < 0:
                    messages.error(request, (
                        f"The {product.name} in your cart\
                            stock quantity changed. Curently\
                                {product.item_count} available"))
                    order.delete()
                    return redirect(reverse('cart'))
                else:
                    order_line = OrderLine(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line.save()
                    stock = product.item_count - quantity
                    product.item_count = stock
                    product.save()

            except Product.DoesNotExist:
                messages.error(request, (
                    "One of the products in your cart\
                            wasn't found in our database."))
                order.delete()
                return redirect(reverse('cart'))

        return redirect(reverse('checkout_success', args=[order.order_number]))
    else:
        messages.error(
            request, 'There was an error with your form.\
            Please double check your information.')
        return redirect(reverse('cart'))


def checkout_success(request, order_number):
    """
    Handle successful checkouts Save user Profile
    to the order and return success order page
    """
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = request.user
        if not order.user_profile == profile:
            order.user_profile = profile
            order.save()

    if 'cart' in request.session:
        del request.session['cart']

    messages.success(
        request, f'Order successfully processed! \
        Your order number is {order}.')

    template = 'checkout/checkout-success.html'

    context = {
        'order': order,
    }

    return render(request, template, context)
