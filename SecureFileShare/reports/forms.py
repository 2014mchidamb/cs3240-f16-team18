from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Report

class ReportForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ReportForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_tag = False

	class Meta:
		model = Report
		fields = ['name', 'short', 'desc', 'priv']

class FileForm(forms.Form):
	file_field = forms.FileField(
		label = "File",
		widget = forms.ClearableFileInput(attrs={'multiple': True}),
		required = False,
	)
	def __init__(self, *args, **kwargs):
		super(FileForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_tag = False

class AddUserReportForm(forms.Form):
	username = forms.CharField(
		label = "Enter Username",
		max_length = 50,
		required = False,
	)
	def __init__(self, *args, **kwargs):
		super(AddUserReportForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_tag = False

class AddGroupReportForm(forms.Form):
	groupname = forms.CharField(
		label = "Enter Group Name",
		max_length = 50,
		required = False,
	)
	def __init__(self, *args, **kwargs):
		super(AddGroupReportForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_tag = False
