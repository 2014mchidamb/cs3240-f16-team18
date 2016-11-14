from django.conf.urls import url
from profile import views

urlpatterns = [
	url(r'^accounts/profile/edit', views.update_profile, name='update_profile'),
	url(r'^accounts/profile', views.profile, name='profile'),
	url(r'^$', views.index, name='index'),
]
