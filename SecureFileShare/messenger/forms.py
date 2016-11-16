from django import forms

from .models import Message


class SendForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'text', 'encryptedFlag']
