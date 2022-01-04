"""
    1. Custemort app Edit profile information form
    2. Custemort app user address form
"""
from django.contrib.auth.models import User
from django import forms
from .models import UserAddress


class EditProfileForm(forms.ModelForm):
    """Edit profile information form"""

    class Meta:
        """User model meta class form"""
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

        for field in self.fields:
            placeholder = self.fields[field].label
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = False


class UserAddressForm(forms.ModelForm):
    """user address form"""

    class Meta:
        """UserAddress model meta class form"""
        model = UserAddress
        exclude = ('user',)
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Placeholders and classes, labels
        """
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field != 'country':

                placeholder = self.fields[field].label
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = False
