# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-05 06:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0003_message_read'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='encryptedFlag',
            new_name='encrypted',
        ),
    ]