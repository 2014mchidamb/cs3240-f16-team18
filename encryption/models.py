from __future__ import unicode_literals
from profile.models import User
from reports.models import ReportFile

from django.db import models

# Create your models here.
class PublicKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE())
    public_key = models.TextField(max_length=1024, default="")

class FileKey(models):
    public_key = models.ForeignKey(PublicKey, on_delete=models.CASCADE)
    file_key = models.TextField(max_length=128, default="")
    file = models.ForeignKey(ReportFile, on_delete=models.CASCADE)

