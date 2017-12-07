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

    @property
    def location(self):
        result = []
        if self.city:
            result.append(self.city.title())
        if self.state:
            result.append(self.state.title())
        if self.country:
            result.append(self.country.title())
        return ", ".join(result)

    class Meta:
        abstract = True

class MentorProfile(Profile):
    experience = models.ManyToManyField('Experience', blank=True)
    professional_experience = models.TextField(blank=True, null=True)
    #course = models.ManyToManyField('Course', blank=True)

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
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u'%s' % self.name

class Languages(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return u'%s' % self.name

class Conversation(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user')
    to_user = models.ForeignKey(User, related_name='to_user')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    parent = models.ForeignKey('self', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u'%s - %s' % (self.from_user, self.to_user)

"""

class CourseMemberIntermediate(models.Model):
    message = models.ForeignKey('Conversation', blank=True)
    member = models.ForeignKey(User)
    course = models.ForeignKey(Course)

class CourseGroup(models.Model):
    name = models.CharField(max_length=150)
    member = models.ManyToManyField(User)
    messages = models.ManyToManyField('Conversation', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CourseGroupIntermediate(models.Model):
    course = models.ForeignKey(Course)
    group = models.ForeignKey(CourseGroup)

class CourseGroup(models.Model):
    #name = models.CharField(max_length=150)
    members = models.ManyToManyField(User)
    messages = models.ManyToManyField('Conversation', blank=True)
    videos = models.ManyToManyField('Videos', blank=True)
    files = models.ManyToManyField('Files', blank=True)

class CourseGroupIntermediate(models.Model):
    course = models.ForeignKey('Course')
    group = models.ForeignKey(CourseGroup)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % self.course, self.group"""

class Certificates(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return "%s" % (self.name)

class Course(models.Model):
    owner = models.ForeignKey(User, related_name='course_owner')
    title = models.CharField(max_length=150)
    description = models.TextField()
    logo = models.ImageField(upload_to='uploads/course/logos/%y/%m/%d', blank=True, null=True)
    #joiners = models.ManyToManyField(EntrepreneurProfile, blank=True)
    #members = models.ManyToManyField(User, through='CourseMemberIntermediate')
    #groups = models.ManyToManyField('CourseGroup', through='CourseGroupIntermediate')
    members = models.ManyToManyField(User, blank=True, related_name='course_members')
    messages = models.ManyToManyField('Conversation', blank=True)
    videos = models.ManyToManyField('Videos', blank=True)
    files = models.ManyToManyField('Files', blank=True)
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.title, self.owner)

class Training(models.Model):
    course = models.ForeignKey(Course)
    #certificates = models.ManyToManyField('Certificates')

class UserTraining(models.Model):
    training = models.ForeignKey(Training)
    user = models.ForeignKey(User)
    awarded_certificates = models.ManyToManyField('Certificates')

class Videos(models.Model):
    video = models.FileField(upload_to="uploads/course/video/%y/%m/%d")
    created_at = models.DateTimeField(auto_now_add=True)

class Files(models.Model):
    file = models.FileField(upload_to="uploads/course/files/%y/%m/%d")
    created_at = models.DateTimeField(auto_now_add=True)
