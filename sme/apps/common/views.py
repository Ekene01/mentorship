# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.views.generic.edit import FormView, View, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.forms import modelformset_factory
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q


# Local imports
#from .signals import new_profile
from .forms import (RegistrationForm, EntrepreneurProfileEditForm, ExperienceForm,
                    ConversationForm, SearchForm, CourseForm)
from .models import EntrepreneurProfile, MentorProfile, Experience, Course
from apps.utils import get_object_or_None, send_mail_html, get_base_url

def get_profile(kwargs):
    print(kwargs)
    try:
        profile = EntrepreneurProfile.objects.get(**kwargs)
        is_mentor = False
    except EntrepreneurProfile.DoesNotExist:
        profile = MentorProfile.objects.get(**kwargs)
    return profile

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
        pk = self.kwargs['pk']
        is_mentor = True
        try:
            profile = EntrepreneurProfile.objects.get(id=pk)
            is_mentor = False
        except EntrepreneurProfile.DoesNotExist:
            profile = MentorProfile.objects.get(id=pk)

        experience_formset = modelformset_factory(Experience, form=ExperienceForm, extra=1)
        experience_formset = experience_formset(queryset=profile.experience.all())
        #print(experience_formset, "EF")
        context.update(pk=self.kwargs['pk'],
                       experience_formset=experience_formset)
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
        return HttpResponseRediConversationrect(reverse('edit-profile', kwargs={'pk': self.kwargs['pk']}))"""

class ConversationView(FormView):
    form_class = ConversationForm
    template_name = 'common/conversation.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ConversationView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ConversationView, self).get_context_data(*args, **kwargs)
        profile = get_profile({'user__id': self.kwargs['to_user_id']})
        context.update(profile=profile)
        return context

    def form_valid(self, form):
        subject = 'SME: New message'
        html_name = 'email/message_notification.html'
        text_name = 'email/message_notification.txt'
        to_user = get_object_or_404(User, id=self.kwargs['to_user_id'])
        new_message = form.save(commit=False)
        new_message.from_user = self.request.user
        new_message.to_user = to_user
        new_message.save()
        """send_mail_html(subject,
                       [to_user.email],
                       html_name,
                       text_name,
                       context_dict={'from_user_first_name': self.request.user.first_name.title(),
                                     'to_user_first_name': to_user.first_name.title(),
                                     'message': new_message.message,
                                     'BASE_URL': get_base_url(self.request),
                                     'from_user_id': self.request.user.id})"""
        messages.success(self.request, "The message is sent successfully!")
        return HttpResponseRedirect(reverse('conversation', kwargs={'to_user_id': self.kwargs['to_user_id']}))

class SearchView(View):

    def get(self, request, *args, **kwargs):
        context = {'form': SearchForm(self.request.GET)}
        get_dict = self.request.GET
        print(get_dict)
        if self.kwargs['whom'] == 'group':
            self.template_name = 'common/search_group.html'
        elif self.kwargs['whom'] == 'profile':
            self.template_name = 'common/search.html'
        #print(self.template_name)
        if self.kwargs['whom'] == 'group':
            results = Course.objects.all()
            if 'keywords' in get_dict and get_dict['keywords']:
                results = results.filter(Q(title__icontains=get_dict['keywords']) | Q(description__icontains=get_dict['keywords']))
            context.update(results=results)
        else:
            profiles = MentorProfile.objects.all()
            if 'industry' in get_dict and get_dict['industry']:
                profiles = profiles.filter(industry__name__icontains=get_dict['industry'])
            if 'country' in get_dict and get_dict['country']:
                profiles = profiles.filter(country=get_dict['country'])
            if 'languages_spoken' in get_dict and get_dict['languages_spoken']:
                profiles = profiles.filter(languages_spoken__name__icontains=get_dict['languages_spoken'])
            if 'keywords' in get_dict and get_dict['keywords']:
                profiles = profiles.filter(Q(user__first_name__icontains=get_dict['keywords']) | Q(user__last_name__icontains=get_dict['keywords']))
            print(profiles, "PROFILES!")
            context.update(profiles=profiles)
        return render(self.request, self.template_name, context)

class AddGroupView(FormView):
    form_class = CourseForm
    template_name = 'common/add_group.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddGroupView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.owner = self.request.user
        form.save()
        return HttpResponseRedirect(reverse('profile'))

class GroupDetailView(UpdateView):
    model = Course
    template_name = 'common/group-detail.html'
    fields = ('id',)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GroupDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(GroupDetailView, self).get_context_data(*args, **kwargs)
        current_user = self.request.user
        if self.object.members.filter(id=current_user.id).exists():
            context.update(is_joined=True)
        if self.object.owner_id == current_user.id:
            context.update(is_owner=True)
        print(context, self.object.owner_id,current_user.id, current_user.id )
        return context

    def post(self, *args, **kwargs):
        current_user = self.request.user
        #print(dir(self))
        self.get_object().members.add(current_user)
        #self.object.save()
        #print(self.request.user)
        messages.success(self.request, "You have joined this group successfully!")
        return HttpResponseRedirect(reverse('group-detail', kwargs={'pk': self.kwargs['pk']}))

