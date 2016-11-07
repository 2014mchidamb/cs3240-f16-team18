from django.conf.urls import url
from reports import views

urlpatterns = [
	url(r'^myreports', views.view_my_reports, name='view_my_reports'),
	url(r'^$', views.index, name='index'),
]
