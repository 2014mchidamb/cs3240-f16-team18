from django.db import models

# Create your models here.
class ReportsTree(models.Model):
	owner = models.OneToOneField(Profile, on_delete=models.CASCADE)
	treeStruct = models.TextField()
