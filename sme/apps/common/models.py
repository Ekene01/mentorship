# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User)
    address = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.user