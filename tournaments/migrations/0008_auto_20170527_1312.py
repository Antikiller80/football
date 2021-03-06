# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-27 10:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0007_auto_20170518_2107'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='matches',
            options={'ordering': ['tour', 'match_date'], 'verbose_name': 'матч', 'verbose_name_plural': 'матчи'},
        ),
        migrations.AlterModelOptions(
            name='matchevent',
            options={'ordering': ['event_time'], 'verbose_name': 'событие матча', 'verbose_name_plural': 'события матча'},
        ),
        migrations.AlterField(
            model_name='matches',
            name='сhampionship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='league', to='tournaments.Championship', verbose_name='Чемпионат'),
        ),
    ]
