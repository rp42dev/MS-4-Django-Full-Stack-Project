from django import forms
from .models import Product, Category


class ItemForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='image', required=False)
   
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
                placeholder = field_name
            field.widget.attrs['placeholder'] = placeholder
            field.widget.attrs['class'] = 'form-control'