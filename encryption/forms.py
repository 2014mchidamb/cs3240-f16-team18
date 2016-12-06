from django import forms
from .models import PublicKey, FileKey

class PublicKeyForm(forms.ModelForm):

	class Meta:
		model = PublicKey
		fields = ['user', 'public_key']

class FileKeyForm(forms.ModelForm):

	class Meta:
		model = FileKey
		fields = ['public_key', 'file_key', 'file']