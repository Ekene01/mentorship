'''
Add signals here!
'''

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import EntrepreneurProfile, MentorProfile

@receiver(post_save, sender=User)
def new_profile(sender, instance, created, **kwargs):
    if created:

        Profile.objects.create(user=instance)