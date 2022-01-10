"""
Handle Stripe webhookse
    1. Handle a generic/unknown/unexpected webhook event
    2. Handle the payment_intent.succeeded webhook from Stripe
    3. Handle the payment_intent.payment_failed webhook
"""
import json
import time
import stripe

from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from shop.models import Product
from .models import Order, OrderLine


class StripeWhHandler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order, success):
        """Send the user a confirmation email"""

        customer_email = order.email
        if success:
            subject = (f'A Hat Shop Confirmation or'
                       f'Order Number { order.order_number }')

            body = render_to_string(
                'checkout/confirmation_emails/confirmation_email_body.txt',
                {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        else:
            subject = (f'A Hat Shop Order payment failed for'
                       f'Order Number { order.order_number }')

            body = render_to_string(
                'checkout/confirmation_emails/failed_email_body .txt',
                {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        Check if order exists in the database if not create order
        after create Send order confirmation email to the customer.
        """
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        total = round(intent.charges.data[0].amount / 100, 2)
        paid = intent.charges.data[0].paid

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        profile = None
        order_exists = False
        attempt = 1

        while attempt <= 5:
            try:
                order = Order.objects.get(stripe_pid=pid)

                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order, True)
            if paid:
                order.status = 'Payment received'
            order.paid = paid
            order.save()
            return HttpResponse(
                content=f'Webhook received: {event["type"]}\
                    | SUCCESS: Verified order already in database',
                        status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    user_profile=profile,
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    address_line_1=shipping_details.address.line1,
                    address_line_2=shipping_details.address.line2,
                    city=shipping_details.address.city,
                    county=shipping_details.address.state,
                    postcode=shipping_details.address.postal_code,
                    country=shipping_details.address.country,
                    paid=paid,
                    total=total,
                    items=cart,
                    stripe_pid=pid,
                )
                if paid:
                    order.status = 'Payment received'
                    order.paid = paid
                    order.save()
                for item_id, quantity in json.loads(cart).items():
                    try:
                        product = Product.objects.get(id=item_id)
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
                        return HttpResponse(
                            content=(f'Webhook received: {event["type"]}'
                                     f' | ERROR: creating order Product'
                                     f' {product} does not exist'), status=500)

            except Exception as error:
                if order:
                    order.delete()
                return HttpResponse(
                    content=(f'Webhook received: {event["type"]}'
                             f' | ERROR: {error}'), status=500)

        self._send_confirmation_email(order, True)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS:'
                    f' Verified order already in database', status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook
        If payment failed return items to the inventory
        If order was created mark order status as cancelled
        """
        intent = event.data.object
        pid = intent.id
        intent = stripe.PaymentIntent.retrieve(pid)
        cart = intent.metadata.cart
        order_exists = False
        attempt = 1

        while attempt <= 5:
            try:
                order = Order.objects.get(stripe_pid=pid)
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            order.status = 'Cancelled'
            order.save()
            self._send_confirmation_email(order, False)
            for item_id, quantity in json.loads(cart).items():
                try:
                    product = Product.objects.get(id=item_id)
                    product.item_count += quantity
                    product.save()
                except Product.DoesNotExist:
                    return HttpResponse(
                        content=f'Webhook received: {event["type"]}\
                            | ERROR: Product does not exists', status=200)
            return HttpResponse(
                content=f'Webhook received: {event["type"]}\
                    | SUCCESS: Order Was Cancelled', status=200)
        else:
            order = None
            return HttpResponse(
                content=f'Webhook received: {event["type"]}\
                    | ERROR: Order does not exists', status=200)

        return HttpResponse(
            content=f'Webhook received: {event["type"]}', status=200)
