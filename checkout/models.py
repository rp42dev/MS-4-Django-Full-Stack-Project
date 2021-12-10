import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.utils import timezone

from django.contrib.auth.models import User
from django_countries.fields import CountryField

from shop.models import Product
from customers.models import UserAddress


ORDER_STATUS_CHOICES= (
    ('Pending', 'Pending'),
    ('Shipped', 'Shipped'),
    ('Cancelled', 'Cancelled'),
    ('Refunded', 'Refunded'),
)


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user = models.ForeignKey(UserAddress, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    address_line_1 = models.CharField(max_length=100, null=False, blank=False)
    address_line_2 = models.CharField(max_length=100, null=False, blank=False)
    town = models.CharField(max_length=60, null=False, blank=False)
    county = models.CharField(max_length=60, null=True, blank=True)
    postcode = models.CharField(max_length=30, null=True, blank=True)
    country = CountryField(blank_label='Country', null=False, blank=False)
    date = models.DateTimeField(default=timezone.now)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    status = models.CharField(max_length=120, default='pending', choices= ORDER_STATUS_CHOICES)
  
    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(Sum('item_total'))['item_total__sum'] or 0
        if self.order_total < 50:
            self.delivery_cost = self.order_total * 10 / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = uuid.uuid4().hex.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLine(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    item = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    item_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        and update the order total.
        """
        if self.item.sale:
            self.item_total = self.item.sale_price * self.quantity
        else:
            self.item_total = self.item.price * self.quantity
        super().save(*args, **kwargs)