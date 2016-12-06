from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Report(models.Model):
	name = models.CharField(max_length=30, blank=True)
	tstamp = models.DateTimeField(auto_now=True)
	short = models.CharField(verbose_name="Short Description", max_length=50, blank=True)
	desc = models.TextField(verbose_name="Summary", max_length=500, blank=True)
	priv = models.BooleanField(verbose_name="private", default=False)
	owners = models.ManyToManyField(User, related_name="owners", through="Ownership")
	viewers = models.ManyToManyField(User, related_name="viewers", through="Viewership")

class ReportFile(models.Model):
	rfile = models.FileField(blank=True)
	reports = models.ManyToManyField(Report, through="Fileship")
	rhash = models.TextField(max_length=100, default="")

class Fileship(models.Model):
	report = models.ForeignKey(Report, on_delete=models.CASCADE)
	repfile = models.ForeignKey(ReportFile, on_delete=models.CASCADE)

class Ownership(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	report = models.ForeignKey(Report, on_delete=models.CASCADE)

class Viewership(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	report = models.ForeignKey(Report, on_delete=models.CASCADE)
