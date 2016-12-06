from django.conf.urls import url
from messenger import views

urlpatterns = [
    url(r'^encryption/add_publickey', views.add_publickey, name='add_publickey'),
    url(r'^encryption/get_publickey', views.get_publickey, name='get_publickey'),
    url(r'^encryption/add_filekey', views.add_filekey, name='add_filekey'),
    url(r'^encryption/get_filekey', views.get_filekey, name='get_filekey'),
    url(r'^encryption/get_target_keys', views.get_target_keys, name='get_target_keys'),
]
