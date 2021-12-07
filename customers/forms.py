from django import forms
from .models import UserAddress
from django.contrib.auth.models import User

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
                'email',
                'first_name',
                'last_name',
        )
    def __init__(self, *args, **kwargs):
        """
        Placeholders and classes, labels 
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'email': 'Email Address',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = False


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Placeholders and classes, labels 
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            
            'address_line_1': 'Street Address 1',
            'address_line_2': 'Street Address 2',
            'town': 'Town or City',
            'postcode': 'Postal Code',
            'county': 'County, State or Locality',
        }

        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = False