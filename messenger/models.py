from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Message(models.Model):
    text = models.TextField(max_length=500, blank=True)
    sender = models.CharField(max_length=50, blank=True)
    recipient = models.CharField(max_length=50, blank=True)
    encryptedFlag = models.BooleanField(default=False)

    def __str__(self):
        return str(self.text)

