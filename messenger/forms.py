from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Message

class SendForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(SendForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_tag = False

	class Meta:
		model = Message
		fields = ['recipient', 'text', 'encryptedFlag']
