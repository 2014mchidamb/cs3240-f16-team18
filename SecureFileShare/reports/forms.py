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
		fields = ['name', 'short', 'desc']

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
