# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 06:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_auto_20171120_0342'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
