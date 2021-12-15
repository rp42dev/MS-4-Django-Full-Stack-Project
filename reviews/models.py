from django.db import models
from django.contrib.auth.models import User
from checkout.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


class ProductReview(models.Model):
    user_profile = models.ForeignKey(
        User, on_delete=models.DO_NOTHING,
        related_name='user_review')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='product_review')
    rating = models.SmallIntegerField(default=5)
    review = models.TextField(
        max_length=500, null=False,
        blank=False, default='')
    date = models.DateTimeField(auto_now_add=True)
