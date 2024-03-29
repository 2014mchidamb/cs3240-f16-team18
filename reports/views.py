from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, render_to_response, HttpResponse
from django.template import RequestContext
from .forms import ReportForm, FileForm, AddUserReportForm, AddGroupReportForm, AddFolderForm
from .models import Folder, Report, ReportFile, Fileship, Ownership, Viewership, Reportship
from django.views.static import serve
from django.contrib.auth import authenticate
import os

from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required
def reports(request):
	if not request.user.profile.active:
		return render(request, template_name='suspended.html')
	myreports = Report.objects.filter(viewers__username__exact=request.user.username)
	myfolders = Folder.objects.filter(username=request.user.username)
	if request.user.profile.site_manager:
		myreports = Report.objects.all()
	if 'create_folder' in request.POST:
		create_folder_form = AddFolderForm(request.POST)
		if create_folder_form.is_valid():
			f = Folder(name=create_folder_form.cleaned_data['foldername'], username=request.user.username)
			f.save()
			return redirect('/accounts/reports/')
	else:
		create_folder_form = AddFolderForm()
	return render(request, 'reports/reports.html', {
			'myreports': myreports,
			'myfolders': myfolders,
			'create_folder_form': create_folder_form
	})

@csrf_exempt
def fda_login(request):
	requested = request.POST
	user = authenticate(username=requested['username'], password=requested['password'])
	if user is not None:
		return render(request, template_name='reports/filemake.html', context={"fileData": "SUCCESS"})
	else:
		return render(request, template_name='reports/filemake.html', context={"fileData": "FAILURE"})



@csrf_exempt 
def file_verify(request):
	requested = request.POST
	user = requested['user']
	report_name = requested["report"]
	file_name = requested["file"]
	
	report = Report.objects.get(name=report_name)
	
	user_files = ReportFile.objects.filter(reports__name__exact=report_name)
	for fil in user_files:
		if (fil.rfile.name == file_name or fil.rfile.name == file_name+".enc"):
			return render(request, template_name='reports/filemake.html', context={"fileData": fil.rhash})
	return render(request, template_name='reports/filemake.html', context={"fileData": "No file found within requested report."})

@csrf_exempt 
def desc_get(request):
	requested = request.POST
	user_name   = requested['user']
	report_name = requested['report']
	
	report = Report.objects.get(name=report_name)
	return render(request, template_name='reports/filemake.html', context={"fileData": report.desc})
	
	
@csrf_exempt 
def file_get(request):
	requested = request.POST
	user = requested['user']
	report_name = requested["report"]
	file_name = requested["file"]
	
	report = Report.objects.get(name=report_name)
	cant_view = report.priv and not report.viewers.filter(username=request.user.username)
	
	cant_view = False#need auth works
	
	if cant_view:
		return render(request, template_name='reports/filemake.html', context={"fileData": "You do not have permissions"})
		
		
	user_files = ReportFile.objects.filter(reports__name__exact=report_name)
	list_names = []
	for fil in user_files:
		if (fil.rfile.name == file_name):
			filepath = "./media/"+fil.rfile.url
			print(os.path.basename(filepath))
			return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
			#return render(request, template_name='reports/filemake.html', context={"fileData": fil.rfile.open()})

	return render(request, template_name='reports/filemake.html', context={"fileData": "No file found within requested report."})

@csrf_exempt 
def file_list(request):
	requested = request.POST
	user_name   = requested['user']
	report_name = requested['report']
	
	if report_name == "ALL`REP":
		myreports = Report.objects.filter(viewers__username__exact=user_name)
		list_names = []
		for reps in myreports:
			list_names.append(reps.name+": "+reps.short)
		
		dispVal = (str(list_names)).replace("'","")
		return render(request, template_name='reports/filemake.html', context={"fileData": dispVal})
		
	usersFiles = ReportFile.objects.filter(reports__name__exact=report_name)
	
	if len(usersFiles) == 0:
		return render(request, template_name='reports/filemake.html', context={"fileData": "No such report"})
	
	report = Report.objects.get(name=report_name)
	
	cant_view = report.priv and not report.viewers.filter(username=request.user.username)
	
	cant_view = False #whyyy
	
	if cant_view:
		return render(request, template_name='reports/filemake.html', context = {"fileData": "You do not have permisions!"})
	
	print(usersFiles)
	
	#if len(usersFiles) == 0:
		#newFile = Files(owner = request.user.username, name = "ReadMe.txt", fileCont = "Welcome to SecureFileShare.  Try uploading more files here.")
		#newFile.save()
		#return file_list(request)
	
	list_names = []
	for files in usersFiles:
		list_names.append(files.rfile.name)
		
	dispVal = (str(list_names)).replace("'","")
	
	return render(request, template_name='reports/filemake.html', context={"fileData": dispVal})

@csrf_exempt 
def file_upload(request):
	requested = request.POST
	report_name = requested['rep_name']
	hashy = requested['hashy']
	
	rep = Report.objects.get(name=report_name)
	
	if rep == None:
		return render(request, template_name='reports/filemake.html', context = {"fileData": "No such report!"})
	
	cant_touch = not rep.owners.filter(username=request.user.username)
	print(request.user.username)
	print(cant_touch)
	
	cant_touch=False#don't know why it is broke....
	
	if cant_touch:
		return render(request, template_name='reports/filemake.html', context = {"fileData": "You do not have permisions!"})
	
	print(request.FILES)
	
	upl = request.FILES.getlist('files')[0]
	
	rfile = ReportFile(rfile=upl, rhash=hashy)
	rfile.save()
	fship = Fileship(report=rep, repfile=rfile)
	fship.save()
	
	return render(request, template_name='reports/filemake.html', context={"fileData": "success"})

@login_required
def create_reports(request):
	if not request.user.profile.active:
		return render(request, template_name='suspended.html')
	if request.method == 'POST':
		report_form = ReportForm(request.POST)
		if report_form.is_valid():
			report_form.save()
			rep = Report.objects.get(name=report_form.cleaned_data['name'])
			own = Ownership(user=request.user, report=rep)
			vw = Viewership(user=request.user, report=rep)
			own.save()
			vw.save()

			for f in request.FILES.getlist('files'):
				rfile = ReportFile(rfile=f)
				rfile.save()
				fship = Fileship(report=rep, repfile=rfile) #Verify only works with standalone
				fship.save()
			messages.success(request, 'You successfully created a report!')
			return redirect('/accounts/reports/')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		report_form = ReportForm()	
	return render(request, 'reports/create_reports.html', {
		'report_form': report_form
	})

@login_required
def edit_report(request, report_name):
	if not request.user.profile.active:
		return render(request, template_name='suspended.html')
	report = Report.objects.get(name=report_name)
	is_owner = report.owners.filter(username=request.user.username)
	if request.user.profile.site_manager:
		is_owner = True	
	if request.method == 'POST':
		report_form = ReportForm(request.POST, instance=report)
		if report_form.is_valid():
			report_form.save()

			for f in request.FILES.getlist('files'):
				rfile = ReportFile(rfile=f)
				rfile.save()
				fship = Fileship(report=report, repfile=rfile)
				fship.save()
			return redirect('/accounts/reports/')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		report_form = ReportForm(instance=report)
	return render(request, 'reports/edit_reports.html', {
		'report_form': report_form,
		'cant_edit': not is_owner
	})

@login_required
def view_folder(request, folder_name):
	if not request.user.profile.active:
		return render(request, template_name='suspended.html')
	folder = Folder.objects.get(name=folder_name)
	cant_view = not (folder.username == request.user.username)
	if request.user.profile.site_manager:
		cant_view = False
	if 'delete' in request.POST:
		folder.delete()
		return redirect('/accounts/reports/')
	return render(request, 'reports/folder_profile.html', {
		'folder': folder, 
		'reports': folder.reports.all(),
		'cant_view': cant_view
	})

@login_required
def view_report(request, report_name):
	if not request.user.profile.active:
		return render(request, template_name='suspended.html')
	report = Report.objects.get(name=report_name)
	is_owner = report.owners.filter(username=request.user.username)
	cant_view = report.priv and not report.viewers.filter(username=request.user.username)
	if request.user.profile.site_manager:
		is_owner = True
		cant_view = False
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
	if 'add_folder' in request.POST:
		add_folder_form = AddFolderForm(request.POST)
		if add_folder_form.is_valid():
			folder_to_add = Folder.objects.filter(name=add_folder_form.cleaned_data['foldername']).first()
			if folder_to_add:
				r = Reportship(folder=folder_to_add, report=report)
				r.save()
			return redirect('/reports/'+report_name)
	else:
		add_folder_form = AddFolderForm()
	if 'delete' in request.POST:
		report.delete()
		return redirect('/accounts/reports')
	return render(request, 'reports/report_profile.html', {
		'report': report,
		'is_owner': is_owner,
		'cant_view': cant_view,
		'private': report.priv,
		'files': ReportFile.objects.filter(reports__name__exact=report_name),
		'viewers': report.viewers.all(),
		'add_user_form': add_user_form,
		'add_group_form': add_group_form,
		'add_folder_form': add_folder_form
	})

@login_required
def public_reports(request):
	if not request.user.profile.active:
		return render(request, template_name='suspended.html')
	pubreps = Report.objects.filter(priv=False)
	return render(request, 'reports/public_reports.html', {
		'pubreps': pubreps
	})
