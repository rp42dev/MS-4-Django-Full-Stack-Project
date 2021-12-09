from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 
                'address_line_1', 'address_line_2',
                'town', 'county', 'postcode',
                'country',)

    def __init__(self, *args, **kwargs):
        """
        form for checkout page
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