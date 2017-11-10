# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm

# Local imports
#from .signals import new_profile
from .forms import RegistrationForm


# Create your views here.
class SigninView(LoginView):
    template_name = 'common/login.html'
    form_class = AuthenticationForm

class SignupView(FormView):
    template_name = 'common/register.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        user = form.save()
        #new_profile.send(user=user)
        return HttpResponseRedirect(reverse('login') + "?next=/profile/")

class ProfileView(TemplateView):
    template_name = 'common/profile.html'
