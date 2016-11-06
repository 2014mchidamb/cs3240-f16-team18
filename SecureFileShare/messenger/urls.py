from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^messenger/send', views.send, name='send')
]
