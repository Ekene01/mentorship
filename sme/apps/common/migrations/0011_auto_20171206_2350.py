# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-06 23:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0010_conversation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CourseGroupIntermediate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Course')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.CourseGroup')),
            ],
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/files/%y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='uploads/video/%y/%m/%d')),
            ],
        ),
        migrations.AddField(
            model_name='coursegroup',
            name='files',
            field=models.ManyToManyField(blank=True, to='common.Files'),
        ),
        migrations.AddField(
            model_name='coursegroup',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='coursegroup',
            name='messages',
            field=models.ManyToManyField(blank=True, to='common.Conversation'),
        ),
        migrations.AddField(
            model_name='coursegroup',
            name='videos',
            field=models.ManyToManyField(blank=True, to='common.Videos'),
        ),
        migrations.AddField(
            model_name='course',
            name='groups',
            field=models.ManyToManyField(through='common.CourseGroupIntermediate', to='common.CourseGroup'),
        ),
        migrations.AddField(
            model_name='course',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
