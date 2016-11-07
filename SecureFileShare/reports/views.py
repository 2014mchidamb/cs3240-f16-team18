from django.contrib.auth.decorators import login_required
from django.shortcuts import render
#from .models import ReportsTree

# Create your views here.
def index(request):
	return render(request, template_name='index.html')

@login_required
def view_my_reports(request):
	#treeDisp = User.objects.all()
	return render(request, template_name='reports/directory.html',) #context={'treeStruct': treeDisp})
