# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-05 06:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0007_profile_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='priv_key',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='profile',
            name='pub_key',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]
