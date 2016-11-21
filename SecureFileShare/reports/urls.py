from django.conf.urls import url
from reports import views

urlpatterns = [
	#url(r'myreports/([0-9]{8})/$', views.file_get),
	url(r'file_get', views.file_get, name='file_get'),
	url(r'file_list', views.file_list, name='file_list'),
	url(r'file_upload', views.file_upload, name='file_upload'),
	url(r'^accounts/reports/create', views.create_reports, name='create_reports'),
	url(r'^accounts/reports', views.reports, name='reports'),
	url(r'^reports/(?P<report_name>.+)', views.view_report, name='view_report'),
]
