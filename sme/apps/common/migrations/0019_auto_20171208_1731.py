# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-08 17:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0018_auto_20171208_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentorprofile',
            name='company',
            field=models.CharField(default='nice', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='postal_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
