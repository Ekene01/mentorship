# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.

from django.contrib.auth.models import User

COUNTRY_CHOICES = [
    ('', '-- Select --'),
    ('NI', 'Nigeria'),
    ('US', 'United States'),
    ('IN', 'India')
]

GENDER_CHOICES = [
    ('', '-- Select --'),
    ('m', 'Male'),
    ('f', 'Female'),
    ('o', 'Other'),
    ('n', "I'd prefer not to share")
]

cur_year = datetime.today().year
BIRTH_YEAR_CHOICES = [('', 'Select'),
                      ('n', "I'd prefer not to share")]
[BIRTH_YEAR_CHOICES.append(('%s' % y, y)) for y in range(cur_year - 15, cur_year - 80)]

class BaseExtraProfile(models.Model):
    experience = models.ManyToManyField('Experience', blank=True, related_name="experience_%(class)ss")
    professional_experience = models.TextField(blank=True, null=True, help_text="Explain about your professional experience!")
    industry = models.ManyToManyField('Industry')
    expert_areas = models.ManyToManyField('ExpertAreas', blank=True, related_name="expert_areas_%(class)ss")

    class Meta:
        abstract= True

class EntrepreneurProfile(BaseExtraProfile):
    need_help = models.TextField(blank=True, null=True)
    pass

class MentorProfile(BaseExtraProfile):
    management_experience = models.IntegerField(blank=True)
    ownership_experience = models.IntegerField(blank=True)
    business_experience_country = models.CharField(max_length=200, choices=COUNTRY_CHOICES, blank=True, null=True)
    website = models.URLField(blank=True)
    company = models.CharField(max_length=100)
    company_role = models.CharField(max_length=50)


class Profile(models.Model):
    user = models.OneToOneField(User)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES, blank=True, null=True)
    postal_code = models.CharField(max_length=6, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    photo = models.ImageField(upload_to='%y/%m/%d', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    birth_year = models.CharField(max_length=4, choices=BIRTH_YEAR_CHOICES, blank=True)
    about_me = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    languages_spoken = models.ManyToManyField('Languages')
    mentor = models.OneToOneField(MentorProfile, blank=True, null=True)
    entreprenuer = models.OneToOneField(EntrepreneurProfile, blank=True, null=True)
    is_mentor = models.BooleanField(default=False)
    agree_terms = models.BooleanField(default=False)

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

    #class Meta:
    #    abstract = True

class Industry(models.Model):
    #profile = models.ForeignKey(Profile)
    name = models.CharField(max_length=50)
    icon_name = models.CharField(max_length=30)

    def __str__(self):
        return '%s' % self.name

class ExpertAreas(models.Model):
    name = models.CharField(max_length=50)

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

    @property
    def from_user_profile(self):
        try:
            profile = EntrepreneurProfile.objects.get(user_id=self.from_user.id)
            is_mentor = False
        except EntrepreneurProfile.DoesNotExist:
            profile = MentorProfile.objects.get(user_id=self.from_user.id)
        return profile

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
    #awarded_certificates = models.ManyToManyField('Certificates', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.title, self.owner)

"""class Training(models.Model):
    course = models.ForeignKey(Course)
    #certificates = models.ManyToManyField('Certificates')

class UserTraining(models.Model):
    training = models.ForeignKey(Training)
    user = models.ForeignKey(User)
    awarded_certificates = models.ManyToManyField('Certificates')"""

class Videos(models.Model):
    video = models.FileField(upload_to="uploads/course/video/%y/%m/%d")
    created_at = models.DateTimeField(auto_now_add=True)

class Files(models.Model):
    file = models.FileField(upload_to="uploads/course/files/%y/%m/%d")
    created_at = models.DateTimeField(auto_now_add=True)
