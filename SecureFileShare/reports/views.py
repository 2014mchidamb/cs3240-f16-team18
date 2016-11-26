from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Files
from django.shortcuts import redirect, render, render_to_response, HttpResponse
from django.template import RequestContext
from .forms import ReportForm, FileForm, AddUserReportForm, AddGroupReportForm
from .models import Report, Ownership, Viewership

from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required
def reports(request):
	myreports = Report.objects.filter(viewers__username__exact=request.user.username)
	return render(request, 'reports/reports.html', {
			'myreports': myreports
	})

def file_get(request):
	requested = request.GET
	gotten = requested.get('name')
	
	usersFiles = Files.objects.filter(owner__iexact=request.user.username)
	
	print("uname", request.user.username)
	
	nameMatch = None
	for item in usersFiles:
		if item.name == gotten:
			nameMatch = item
			break
	
	if nameMatch is None:
		return render(request, template_name='reports/filemake.html', context={"fileData": ""})
	
	content_load = nameMatch.fileCont
	
	return render(request, template_name='reports/filemake.html', context={"fileData": content_load})

def file_list(request):
	usersFiles = Files.objects.filter(owner__iexact=request.user.username)
	print(usersFiles)
	
	if len(usersFiles) == 0:
		newFile = Files(owner = request.user.username, name = "ReadMe.txt", fileCont = "Welcome to SecureFileShare.  Try uploading more files here.")
		newFile.save()
		return file_list(request)
	
	list_names = []
	for files in usersFiles:
		list_names.append(files.name)
		
	dispVal = (str(list_names)).replace("'","")
	
	return render(request, template_name='reports/filemake.html', context={"fileData": dispVal})

@csrf_exempt 
def file_upload(request):
	requested = request.POST
	gotten = requested['name']
	cont   = requested['cont']
	print(gotten,cont)
	newFile = Files(owner = request.user.username, name = gotten, fileCont = cont)
	newFile.save()
	
	return render(request, template_name='reports/filemake.html', context={"fileData": "success"})

@login_required
def create_reports(request):
	if request.method == 'POST':
		report_form = ReportForm(request.POST)
		file_form = FileForm(request.POST)
		if report_form.is_valid() and file_form.is_valid():
			report_form.save()
			rep = Report.objects.get(name=report_form.cleaned_data['name'])
			own = Ownership(user=request.user, report=rep)
			vw = Viewership(user=request.user, report=rep)
			own.save()
			vw.save()
			for f in request.FILES.getlist('file_field'):
				print f
			messages.success(request, 'You successfully created a report!')
			return redirect('/accounts/reports/')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		report_form = ReportForm()
		file_form = FileForm()
	return render(request, 'reports/create_reports.html', {
		'report_form': report_form,
		'file_form': file_form
	})

@login_required
def view_report(request, report_name):
	report = Report.objects.get(name=report_name)
	is_owner = report.owners.filter(username=request.user.username)
	cant_view = not report.viewers.filter(username=request.user.username)
	if 'add_user_report' in request.POST:
		add_user_form = AddUserReportForm(request.POST)
		if add_user_form.is_valid():
			user_to_add = User.objects.filter(username=add_user_form.cleaned_data['username']).first()
			if user_to_add:
				v = Viewership(user=user_to_add, report=report)
				v.save()
			return redirect('/reports/'+report_name)
	else:
		add_user_form = AddUserReportForm()
	if 'add_group_report' in request.POST:
		add_group_form = AddGroupReportForm(request.POST)
		if add_group_form.is_valid():
			group_to_add = Group.objects.filter(name=add_group_form.cleaned_data['groupname']).first()
			if group_to_add:
				for member in group_to_add.members.all():
					v = Viewership(user=member, report=report)
					v.save()
			return redirect('/reports/'+report_name)
	else:
		add_group_form = AddGroupReportForm()
	return render(request, 'reports/report_profile.html', {
		'report': report,
		'is_owner': is_owner,
		'cant_view': cant_view,
		'viewers': report.viewers.all(),
		'add_user_form': add_user_form,
		'add_group_form': add_group_form
	})
