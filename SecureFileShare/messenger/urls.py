from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^messenger/send_message', views.send, name='send'),
    url(r'^messenger/read', views.read, name='read')
]
