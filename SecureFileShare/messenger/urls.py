from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^messenger/send', views.send, name='send'),
    url(r'^messenger/send_message', views.send_message, name='send_message'),
    url(r'^messenger/read', views.read, name='read')
]
