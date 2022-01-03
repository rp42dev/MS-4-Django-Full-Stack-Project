"""
    1. Product review Model
"""
from django.db import models
from django.contrib.auth.models import User
from checkout.models import Product
from checkout.models import Order


class ProductReview(models.Model):
    """
    Product review Model
    returns self sku and order id
    """
    CHOICES = [(i, i) for i in range(6)]
    user_profile = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_review')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='product_review')
    rating = models.PositiveSmallIntegerField(
        default=5, choices=CHOICES)
    review = models.TextField(max_length=500)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='order_review', null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f'Review for product SKU {self.product.sku}'
                f'order id {self.order.id}')
