# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-12 16:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20170412_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='activation_key',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='key_expires',
        ),
    ]