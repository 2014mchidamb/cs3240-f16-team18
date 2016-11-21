from django.conf.urls import url
from reports import views

urlpatterns = [
	url(r'^myreports', views.view_my_reports, name='view_my_reports'),
	#url(r'myreports/([0-9]{8})/$', views.file_get),
	url(r'file_get', views.file_get, name='file_get'),
	url(r'file_list', views.file_list, name='file_list'),
	url(r'file_upload', views.file_upload, name='file_upload'),
	
	
	url(r'^$', views.index, name='index'),
]
