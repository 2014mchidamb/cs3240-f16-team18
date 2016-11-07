from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Profile

class UserForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_method = 'post'
		#self.helper.layout.append(Submit('save', 'Save'))		

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_method = 'post'
		self.helper.layout.append(Submit('save', 'Save'))

	class Meta:
		model = Profile
		fields = ['bio', 'location']
