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

