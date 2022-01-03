"""
    1. review form
"""
from django import forms
from .models import ProductReview


class ReviewForm(forms.ModelForm):
    """
    Product review form
    """
    prefix = 'review'

    class Meta:
        """Meta class for Product review model"""
        model = ProductReview
        fields = ('review',)

    def __init__(self, *args, **kwargs):
        """
        Shipping address form
        labels st to be placeholders
        """
        super().__init__(*args, **kwargs)
