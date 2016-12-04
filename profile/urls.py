from django.conf.urls import url
from profile import views

urlpatterns = [
	url(r'^accounts/groups/create', views.create_groups, name='create_groups'),
	url(r'^accounts/groups', views.groups, name='groups'),
	url(r'^accounts/profile/edit', views.update_profile, name='update_profile'),
	url(r'^accounts/profile', views.profile, name='profile'),
	url(r'^groups/(?P<group_name>.+)/edit', views.edit_group, name='edit_group'),
	url(r'^groups/(?P<group_name>.+)', views.view_group, name='view_group'),
	url(r'^public/groups', views.public_groups, name='public_groups'),
	url(r'^$', views.index, name='index'),
]
