from django.db import models
from django.contrib.auth.models import User
from checkout.models import Product


class ProductReview(models.Model):
    CHOICES = [(i, i) for i in range(6)]
    user_profile = models.ForeignKey(
        User, on_delete=models.DO_NOTHING,
        related_name='user_review')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='product_review')
    rating = models.PositiveSmallIntegerField(
        default=5, choices=CHOICES)
    review = models.TextField(max_length=500)
    order_id = models.PositiveSmallIntegerField(
        editable=False, null=True)
    date = models.DateTimeField(auto_now_add=True)
