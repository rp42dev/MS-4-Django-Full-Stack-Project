from django import forms
from .models import ProductReview


class ReviewForm(forms.ModelForm):
    prefix = 'review'
    class Meta:
        model = ProductReview
        fields = ('review',)

    def __init__(self, *args, **kwargs):
        """
        Shipping address form
        labels st to be placeholders
        """
        super().__init__(*args, **kwargs)

