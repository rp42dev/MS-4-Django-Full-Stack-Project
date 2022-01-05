"""
    1. Checkout app's Shipping form
    2. Checkout app's Contact form
"""
from django import forms
from .models import Order


class ShippingForm(forms.ModelForm):
    """checckout app Shipping form Class"""
    prefix = 'shipping'

    class Meta:
        """Order model meta class"""
        model = Order
        fields = ('shipping_name', 'address_line_1',
                  'address_line_2', 'city',
                  'county', 'postcode',
                  'country',)

    def __init__(self, *args, **kwargs):
        """
        Shipping address form
        labels st to be placeholders
        """
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{self.fields[field].label} *'
                else:
                    placeholder = self.fields[field].label

            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = False


class ContactForm(forms.ModelForm):
    """checckout app Contact form Class"""
    prefix = 'contact'

    class Meta:
        """Order model meta class"""
        model = Order
        fields = ('full_name', 'email',)

    def __init__(self, *args, **kwargs):
        """
        Shipping address form
        labels st to be placeholders
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{self.fields[field].label} *'
            else:
                placeholder = self.fields[field].label
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = False
