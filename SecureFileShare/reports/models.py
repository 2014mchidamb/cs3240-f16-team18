from django.db import models

#from django.contrib.auth.models import User
#from django.db import models
#from django.db.models.signals import post_save
#from django.dispatch import receiver

# Create your models here.
class ReportsTree(models.Model):
	#owner = models.OneToOneField(Profile, on_delete=models.CASCADE)
	owner = models.TextField()
	treeStruct = models.TextField()

class Files(models.Model):
	#owner = models.OneToOneField(Profile, on_delete=models.CASCADE)
	owner    = models.TextField()
	name     = models.TextField()
	fileCont = models.TextField()

#def create_user_tree(sender, instance, created, **kwargs):
#	if created:
#		ReportsTree.objects.create(user=instance)