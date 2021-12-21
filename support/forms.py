from django import forms
from .models import CustomerSuport, Message


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


class MessageForm(forms.ModelForm):
    prefix = 'mesage'

    class Meta:
        model = Message
        fields = ('message',)

    def __init__(self, *args, **kwargs):
        """
        Support Message form
        labels st to be placeholders
        """
        super().__init__(*args, **kwargs)

