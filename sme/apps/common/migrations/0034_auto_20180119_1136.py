# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-19 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0033_auto_20180119_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='end_dt',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
