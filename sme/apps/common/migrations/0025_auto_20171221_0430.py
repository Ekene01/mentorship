# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-21 04:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0024_auto_20171221_0422'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='files',
            field=models.ManyToManyField(blank=True, to='common.Files'),
        ),
        migrations.AddField(
            model_name='course',
            name='videos',
            field=models.ManyToManyField(blank=True, to='common.Videos'),
        ),
    ]
