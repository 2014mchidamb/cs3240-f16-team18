# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-05 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0004_auto_20161205_0621'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='etext',
            field=models.BinaryField(blank=True),
        ),
    ]
