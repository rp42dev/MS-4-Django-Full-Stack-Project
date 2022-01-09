"""
    1. Shop Product item form
    2. Order status form
"""
from django import forms
from checkout.models import Order
from .models import Product, Category


class ItemForm(forms.ModelForm):
    """Shop Product item form"""

    class Meta:
        """Product Model meta slass"""
        model = Product
        exclude = ('sku', 'rating', 'rating_counter',)
        fields = '__all__'

    image = forms.ImageField(label='image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            if field_name != 'category' and\
                 field_name != 'image' and field_name != 'sale':
                if field.required:
                    placeholder = f'{field.label} *'
                else:
                    placeholder = field.label
                field.widget.attrs['placeholder'] = placeholder
            if field_name != 'sale' and field_name != 'item_count':
                field.label = False
            elif field_name == 'item_count':
                field.label
            else:
                field.widget.attrs['class'] = 'me-2 checkboxinput'
            field.label
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control'


class OrderStatusForm(forms.ModelForm):
    """Order status form"""

    class Meta:
        """Order Model meta slass"""
        model = Order
        fields = {
            'status'
        }

    def __init__(self, *args, **kwargs):
        """Save place holders and field widgets"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'py-2'
        self.fields['status'].label = False
