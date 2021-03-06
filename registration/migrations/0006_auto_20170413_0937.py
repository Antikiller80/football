# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-13 06:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_auto_20170413_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='key_expires',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
