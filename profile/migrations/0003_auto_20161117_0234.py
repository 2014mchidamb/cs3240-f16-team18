# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-17 02:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profile', '0002_groupprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('desc', models.TextField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile.Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='groupprofile',
            name='group',
        ),
        migrations.DeleteModel(
            name='GroupProfile',
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(through='profile.Membership', to=settings.AUTH_USER_MODEL),
        ),
    ]