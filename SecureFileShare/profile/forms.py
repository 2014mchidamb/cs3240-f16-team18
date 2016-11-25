from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Group, Profile

class UserForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_tag = False

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_tag = False

	class Meta:
		model = Profile
		fields = ['birth_date', 'location', 'bio']

class GroupForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(GroupForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_tag = False

	class Meta:
		model = Group
		fields = ['name', 'desc', 'priv']

class AddUserForm(forms.Form):
	username = forms.CharField(
		label = "Enter Username",
		max_length = 50,
		required = False,
	)
	def __init__(self, *args, **kwargs):
		super(AddUserForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_tag = False

