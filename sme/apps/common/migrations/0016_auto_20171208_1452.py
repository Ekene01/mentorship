# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-08 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0015_profile_is_mentor'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpertAreas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='entrepreneurprofile',
            name='experience',
            field=models.ManyToManyField(blank=True, related_name='experience_entrepreneurprofiles', to='common.Experience'),
        ),
        migrations.AlterField(
            model_name='mentorprofile',
            name='experience',
            field=models.ManyToManyField(blank=True, related_name='experience_mentorprofiles', to='common.Experience'),
        ),
        migrations.AddField(
            model_name='entrepreneurprofile',
            name='expert_areas',
            field=models.ManyToManyField(blank=True, related_name='expert_areas_entrepreneurprofiles', to='common.ExpertAreas'),
        ),
        migrations.AddField(
            model_name='mentorprofile',
            name='expert_areas',
            field=models.ManyToManyField(blank=True, related_name='expert_areas_mentorprofiles', to='common.ExpertAreas'),
        ),
    ]