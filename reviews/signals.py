"""Signals to update Product model"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import ProductReview


@receiver(post_save, sender=ProductReview)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update product reviews on save
    """
    instance.product.update_rating()


@receiver(post_delete, sender=ProductReview)
def update_on_delete(sender, instance, **kwargs):
    """
    Update product review on delete
    """
    instance.product.update_rating()
