# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import User

COUNTRY_CHOICES = [
    ('', '-- Select --'),
    ('NI', 'Nigeria'),
    ('US', 'United States'),
    ('IN', 'India')
]

class Profile(models.Model):
    user = models.OneToOneField(User)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES, blank=True, null=True)
    industry = models.ManyToManyField('Industry')
    photo = models.ImageField(upload_to='%y/%m/%d', blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    languages_spoken = models.ManyToManyField('Languages')

    def __str__(self):
        return u'%s' % self.user

    class Meta:
        abstract = True

class MentorProfile(Profile):
    experience = models.ManyToManyField('Experience', blank=True)
    professional_experience = models.TextField(blank=True, null=True)

class EntrepreneurProfile(Profile):
    experience = models.ManyToManyField('Experience', blank=True)

class Industry(models.Model):
    #profile = models.ForeignKey(Profile)
    name = models.CharField(max_length=50)
    icon_name = models.CharField(max_length=30)

    def __str__(self):
        return '%s' % self.name

class Experience(models.Model):
    name = models.CharField(max_length=50)
    start_month = models.IntegerField()
    start_year = models.IntegerField()
    end_month = models.IntegerField()
    end_year = models.IntegerField()
    industry = models.ManyToManyField('Industry')
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES)
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True
                                      )

    def __str__(self):
        return u'%s' % self.name

class Languages(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return u'%s' % self.name