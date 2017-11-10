# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from .signals import new_profile


class CommonConfig(AppConfig):
    name = 'common'
    verbose_name = _('common')

    def ready(self):
        post_save.connect(new_profile, sender=User)