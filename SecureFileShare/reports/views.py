from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, template_name='index.html')

@login_required
def view_my_reports(request):
	return render(request, template_name='reports/directory.html')
	
