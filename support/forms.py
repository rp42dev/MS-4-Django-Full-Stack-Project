from django import forms
from .models import CustomerSuport


class SupportForm(forms.ModelForm):
    prefix = 'support'
    class Meta:
        model = CustomerSuport
        fields = ('issue', 'message', )

    def __init__(self, *args, **kwargs):
        """
        Support form
        labels st to be placeholders
        """
        super().__init__(*args, **kwargs)

