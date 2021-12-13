from django import forms
from .models import Order


class ShippingForm(forms.ModelForm):
    prefix = 'shipping'
    class Meta:
        model = Order
        fields = ('shipping_name', 'shipping_address_1',
                  'shipping_address_2', 'shipping_town', 
                  'shipping_county', 'shipping_postcode',
                  'shipping_country',)

    def __init__(self, *args, **kwargs):
        """
        Shipping address form
        labels st to be placeholders
        """
        super().__init__(*args, **kwargs)

        # self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':

                placeholder = self.fields[field].label
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = False


class BillingForm(forms.ModelForm):
    prefix = 'billing'
    class Meta:
        model = Order
        fields = ('billing_name', 'billing_address_1',
                  'billing_address_2', 'billing_town',
                  'billing_county', 'billing_postcode',
                  'billing_country',)
                  

    def __init__(self, *args, **kwargs):
        """
        Billing address form
        labels st to be placeholders
        """
        super().__init__(*args, **kwargs)

        # self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':

                placeholder = self.fields[field].label
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = False


