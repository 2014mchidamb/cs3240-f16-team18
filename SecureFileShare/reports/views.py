from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, render_to_response, HttpResponse
from django.template import RequestContext
from .forms import ReportForm
from .models import Report, Ownership, Viewership

# Create your views here.

@login_required
def reports(request):
	myreports = Report.objects.filter(viewers__username__exact=request.user.username)
	return render(request, 'reports/reports.html', {
			'myreports': myreports
	})

@login_required
def create_reports(request):
	if request.method == 'POST':
		report_form = ReportForm(request.POST)
		if report_form.is_valid():
			report_form.save()
			rep = Report.objects.get(name=report_form.cleaned_data['name'])
			own = Ownership(user=request.user, report=rep)
			vw = Viewership(user=request.user, report=rep)
			own.save()
			vw.save()
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
def view_report(request, report_name):
	report = Report.objects.get(name=report_name)
	return render(request, 'reports/report_profile.html', {
		'report': report,
		'owners': report.owners.all(),
		'viewers': report.viewers.all()
	})
