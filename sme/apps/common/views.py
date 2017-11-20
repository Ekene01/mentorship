# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.forms import modelformset_factory

# Local imports
#from .signals import new_profile
from .forms import RegistrationForm, EntrepreneurProfileEditForm, ExperienceForm
from .models import EntrepreneurProfile, MentorProfile, Experience

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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        is_mentor = True
        context = super(ProfileView, self).get_context_data(*args, **kwargs)

        try:
            profile = EntrepreneurProfile.objects.get(user__id=self.request.user.id)
            is_mentor = False
        except EntrepreneurProfile.DoesNotExist:
            profile = MentorProfile.objects.get(user__id=self.request.user.id)
        context.update(profile=profile,
                       profile_id=profile.id)
        return context


def EditProfileView1(request, pk):
    template_name = 'common/edit_profile.html'

    if request.method == 'POST':
        print(request.POST)
        return HttpResponseRedirect(reverse('edit-profile', kwargs={'pk': pk}))
    else:
        is_mentor = True
        try:
            instance = EntrepreneurProfile.objects.get(id=pk)
            is_mentor = False
        except EntrepreneurProfile.DoesNotExist:
            instance = MentorProfile.objects.get(id=pk)
        # form = self.form_class(initial=self.initial, instance=instance)
        profile_formset = modelformset_factory(MentorProfile, exclude=('user',)) if is_mentor else modelformset_factory(
            EntrepreneurProfile, exclude=('user',))
        return render(request, template_name, {'form_set': profile_formset,
                                                    'is_mentor': is_mentor})

class EditProfileView(FormView):
    form_class = EntrepreneurProfileEditForm
    template_name = 'common/edit_profile.html'

    @method_decorator(login_required)
    def dispatch(self, request, *ar, **kw):
        return super(EditProfileView, self).dispatch(request, *ar, **kw)

    def get_context_data(self, *args, **kwargs):
        context = super(EditProfileView, self).get_context_data(*args, **kwargs)
        #initial = self.initial

        #experience_form = ExperienceForm()
        #profile_formset = modelformset_factory(MentorProfile) if is_mentor else modelformset_factory(EntrepreneurProfile)
        context.update(pk=self.kwargs['pk'])
        return context

    def get_form(self):
        pk = self.kwargs['pk']
        is_mentor = True
        try:
            instance = EntrepreneurProfile.objects.get(id=pk)
            is_mentor = False
        except EntrepreneurProfile.DoesNotExist:
            instance = MentorProfile.objects.get(id=pk)
        return self.form_class(instance=instance, **self.get_form_kwargs())

    def form_valid(self, form):
        print(self.request.POST, self.request.FILES)
        first_name = form.cleaned_data['first_name'].title()
        last_name = form.cleaned_data['last_name'].title()
        form = form.save()
        form.user.first_name = first_name
        form.user.last_name = last_name
        form.user.save()
        return HttpResponseRedirect(reverse('profile'))

    """def form_invalid(self, form):
        print("$$$$$$$$$$ not valid $$$")
        #form.save()
        print(self.request.POST, self.request.FILES)
        print(form.errors)
        return HttpResponseRedirect(reverse('edit-profile', kwargs={'pk': self.kwargs['pk']}))"""