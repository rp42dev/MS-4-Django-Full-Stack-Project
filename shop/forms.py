from django import forms
from .models import Product, Category
from checkout.models import Order


class ItemForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='image')
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        last_sku = Product.objects.last()
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]  
          
        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            if field_name == 'sku':
                placeholder = f'Latest { field_name} is "{last_sku.sku}"'
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
    class Meta:
        model = Order
        fields = {
            'status'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].label = False
