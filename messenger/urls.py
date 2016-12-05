from django.conf.urls import url
from messenger import views

urlpatterns = [
    url(r'^messenger/send', views.send, name='send'),
    url(r'^messenger/read', views.read, name='read')
]
