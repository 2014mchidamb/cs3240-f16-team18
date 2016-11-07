from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Message(models.Model):
    text = models.TextField(max_length=500, blank=True)
    sender = models.OneToOneField(User, on_delete=models.Profile)
    recipient = models.OneToOneField(User, on_delete=models.Profile)
    encryptedFlag = models.BooleanField(default=False)
