# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-20 10:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0021_auto_20171218_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupconversationintermediate',
            name='is_question',
            field=models.BooleanField(default=False),
        ),
    ]
