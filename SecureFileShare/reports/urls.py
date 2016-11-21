from django.conf.urls import url
from reports import views

urlpatterns = [
	url(r'^accounts/reports/create', views.create_reports, name='create_reports'),
	url(r'^accounts/reports', views.reports, name='reports'),
	url(r'^reports/(?P<report_name>.+)', views.view_report, name='view_report'),
]
