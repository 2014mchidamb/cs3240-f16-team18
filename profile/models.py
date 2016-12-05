from __future__ import unicode_literals

from Crypto.PublicKey import RSA
from django.contrib.auth.models import User 
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, blank=True)
	location = models.CharField(max_length=30, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	site_manager = models.BooleanField(default=False)
	active = models.BooleanField(default=True)
	priv_key = models.TextField(max_length=1000, blank=True)
	pub_key = models.TextField(max_length=1000, blank=True)
	unread = models.IntegerField(default=0)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		profile=Profile.objects.create(user=instance)
		key = RSA.generate(1024)
		profile.pub_key = key.publickey().exportKey()
		profile.priv_key = key.exportKey()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

class Group(models.Model):
	name = models.CharField(max_length=30, blank=True, unique=True)
	desc = models.TextField(verbose_name="description", max_length=500, blank=True)
	priv = models.BooleanField(verbose_name="private", default=False)
	creators = models.ManyToManyField(User, related_name='creators', through='Creatorship')
	members = models.ManyToManyField(User, related_name='members', through='Membership')

class Membership(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Creatorship(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
