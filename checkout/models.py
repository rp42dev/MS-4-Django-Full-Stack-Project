"""
Order model:
    1.  Order model User shipping and order details
Line Item Model:
    2. Order Line items Update product total
"""
from django.db import models
from django.conf import settings
from django.db.models import Sum
from django_countries.fields import CountryField

from django.contrib.auth.models import User
from customers.models import UserAddress
from shop.models import Product

import uuid


class Order(models.Model):
    """
    Order model order details order status
    User shipping information and contact details
    Update total each time a line item is added
    accounting for delivery costs.
    """
    SUBMITTED = 'Submitted'
    PAYMENT = 'Payment received'
    PROCESSED = 'Proccessed'
    SHIPPED = 'Shipped'
    CANCELLED = 'Cancelled'
    COMPLETED = 'Completed'

    ORDER_STATUS = [
        (SUBMITTED, 'Submitted'),
        (PAYMENT, 'Payment received'),
        (PROCESSED, 'Proccessed'),
        (SHIPPED, 'Shipped'),
        (CANCELLED, 'Cancelled'),
        (COMPLETED, 'Completed'),
    ]

    # Order Info
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, default=SUBMITTED, choices=ORDER_STATUS)
    order_number = models.CharField(
        max_length=32, null=False, editable=False)
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    delivery = models.DecimalField(
        max_digits=6, decimal_places=2, default=0)
    items = models.TextField(
        null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')
    paid = models.BooleanField(default=False)

    # User
    user_profile = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='orders')

    # User contact info
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)

    # Shipping Address
    shipping_name = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=60)
    county = models.CharField(max_length=60, blank=True)
    postcode = models.CharField(max_length=30, blank=True)
    country = CountryField(blank_label='Country')

    def update_total(self):
        """
        Update total each time a line item is added,
        accounting for delivery costs.
        """
        count_total = self.lineitems.aggregate(
            Sum('product_total'))['product_total__sum'] or 0

        if count_total < 50:
            self.delivery = count_total * 10 / 100
            self.total = count_total + self.delivery
        else:
            self.delivery = 0
            self.total = count_total + self.delivery
        self.delivery = round(self.delivery, 2)
        self.total = round(self.total, 2)
        self.save()

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = uuid.uuid4().hex.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(f'Order #{self.order_number}')


class OrderLine(models.Model):
    """
    Order Line items Update product total
    calculateproduct times quantity to product_total
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='lineitems')
    product_total = models.DecimalField(
        max_digits=6, decimal_places=2, editable=False, default=0)

    def save(self, *args, **kwargs):
        """
        Calculate product times quantity
        and update the Product total.
        """
        if self.product.sale:
            self.product_total = self.product.sale_price * self.quantity
        else:
            self.product_total = self.product.price * self.quantity
        self.product_total = round(self.product_total, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} Product id {self.product.id}'
