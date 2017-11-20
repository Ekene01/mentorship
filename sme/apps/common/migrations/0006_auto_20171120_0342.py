# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 03:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_auto_20171117_1502'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experience',
            name='languages_spoken',
        ),
        migrations.AddField(
            model_name='entrepreneurprofile',
            name='languages_spoken',
            field=models.ManyToManyField(to='common.Languages'),
        ),
        migrations.AddField(
            model_name='mentorprofile',
            name='languages_spoken',
            field=models.ManyToManyField(to='common.Languages'),
        ),
    ]
