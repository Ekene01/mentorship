'''
Add decorators!
'''

from django.http import HttpResponseRedirect
from django.shortcuts import reverse

from common.models import Profile
#from common.views import get_profile

def agree_terms_required(func):
    def wrap(request, *args, **kwargs):
        profile = Profile.objects.filter(user__id=request.user.id)
        print(profile, "profileprofileprofile")
        if profile.exists():
            if profile[0].agree_terms:
                return func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('agree-terms'))
        else:
            return HttpResponseRedirect(reverse('login'))
    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__
    return wrap

