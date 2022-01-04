"""
    1. customer support issues form
    2. customer support issues status form
    3. Customer support Message form
"""
from django import forms
from .models import CustomerSuport, Message


class SupportForm(forms.ModelForm):
    """ustomer support issues form"""
    prefix = 'support'

    class Meta:
        """Model CustomerSuport Meta class"""
        model = CustomerSuport
        fields = ('issue', 'message', )

    def __init__(self, *args, **kwargs):
        """
        Support form
        labels st to be placeholders
        """
        super().__init__(*args, **kwargs)


class IssueStatusForm(forms.ModelForm):
    """ustomer support issues status form"""
    prefix = 'issue_status'

    class Meta:
        """Model CustomerSuport Meta class"""
        model = CustomerSuport
        fields = ('status',)

    def __init__(self, *args, **kwargs):
        """
        Support form
        labels st to be placeholders
        """
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'py-1'


class MessageForm(forms.ModelForm):
    """Customer support Message form"""
    prefix = 'mesage'

    class Meta:
        """Model Message Meta class"""
        model = Message
        fields = ('message',)

    def __init__(self, *args, **kwargs):
        """
        Support Message form
        labels st to be placeholders
        """
        super().__init__(*args, **kwargs)
