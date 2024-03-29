from django.conf.urls import url
from reports import views

urlpatterns = [
	#url(r'myreports/([0-9]{8})/$', views.file_get),
	url(r'file_get', views.file_get, name='file_get'),
	url(r'desc_get', views.desc_get, name='desc_get'),
	url(r'file_verify', views.file_verify, name='file_verify'),
	url(r'file_list', views.file_list, name='file_list'),
	url(r'file_upload', views.file_upload, name='file_upload'),
	url(r'fda_login', views.fda_login, name='fda_login'),
	url(r'^accounts/reports/create', views.create_reports, name='create_reports'),
	url(r'^accounts/reports', views.reports, name='reports'),
	url(r'^reports/(?P<report_name>.+)/edit', views.edit_report, name='edit_report'),
	url(r'^reports/(?P<report_name>.+)', views.view_report, name='view_report'),
	url(r'^folders/(?P<folder_name>.+)', views.view_folder, name='view_folder'),
	url(r'^public/reports', views.public_reports, name='public_reports')
]
