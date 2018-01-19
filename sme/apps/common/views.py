# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests

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
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.template.loader import render_to_string


# Local imports
#from .signals import new_profile
from .forms import (RegistrationForm, MentorProfileEditForm, EntrepreneurProfileEditForm, ExperienceForm,
                    ConversationForm, SearchForm, CourseForm)
from .models import (EntrepreneurProfile, MentorProfile, Experience, Course, Profile, Group, Conversation,
                     GroupConversationIntermediate, Payment, GROUP_MESSAGE)
from apps.utils import get_object_or_None, send_mail_html, get_base_url
from apps.decorators import agree_terms_required

MENTOR_PROFILE_NAME = 'mentor'
ENTREPRENUER_PROFILE_NAME = 'entreprenuer'
PROFILE_MAP = {MENTOR_PROFILE_NAME: MENTOR_PROFILE_NAME,
               ENTREPRENUER_PROFILE_NAME: ENTREPRENUER_PROFILE_NAME}

def get_profile(kwargs):
    print(kwargs)
    try:
        profile = Profile.objects.get(**kwargs)
    except Profile.DoesNotExist:
        profile = None
    return profile

# Create your views here.
class SigninView(LoginView):
    template_name = 'common/login.html'
    form_class = AuthenticationForm

class SignupView(FormView):
    template_name = 'common/register.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        profile = form.save()
        #new_profile.send(user=user)
        #return HttpResponseRedirect(reverse('login') + "?next=/profile/")
        user = authenticate(username=form.cleaned_data['email'],
                            password=form.cleaned_data['password'])
        if user is None:
            return HttpResponseRedirect(reverse('login'))
        else:
            login(self.request, user)
            messages.success(self.request, "You have registered successfully. Please agree terms to continue.")
            return HttpResponseRedirect(reverse('agree-terms'))

class AgreeTermsView(View):
    template_name = 'common/agree_terms.html'
    #form_class = AgreeTermsForm
    #fields = ('agree_terms', )
    #model = Profile

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AgreeTermsView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {}
        profile = Profile.objects.get(user__id=self.request.user.id)
        context.update(user_type = 'mentor' if profile.is_mentor else 'entreprenuer')
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user__id=self.request.user.id)
        profile.agree_terms = True
        profile.save()
        print(profile.id, "PROFILE ID")
        return HttpResponseRedirect(reverse('profile'))

class ViewProfile(TemplateView):

    @method_decorator(login_required)
    @method_decorator(agree_terms_required)
    def dispatch(self, *args, **kwargs):
        return super(ViewProfile, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ViewProfile, self).get_context_data(*args, **kwargs)
        profile = get_profile({'id': self.kwargs['pk']})
        #print(profile.agree_terms, "AGEREEE")
        context.update(is_profile_owner=profile if self.request.user.id == profile.user.id else False,
                       profile=profile,
                       profile_id=profile.id,
                       profile_type=PROFILE_MAP[MENTOR_PROFILE_NAME] if profile.is_mentor else \
                                                                        PROFILE_MAP[ENTREPRENUER_PROFILE_NAME])
        return context

    def get_template_names(self, *ar, **kw):
        profile = get_profile({'id': self.kwargs['pk']})
        template_name = 'common/mentor_profile.html' if profile.is_mentor else 'common/entreprenuer_profile.html'
        return [template_name]

class ProfileView(TemplateView):
    #template_name = 'common/profile.html'

    @method_decorator(login_required)
    @method_decorator(agree_terms_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        profile = get_profile({'user__id': self.request.user.id})
        print(profile.agree_terms, "AGEREEE")
        context.update(profile=profile,
                       profile_id=profile.id,
                       profile_type=PROFILE_MAP[MENTOR_PROFILE_NAME] if profile.is_mentor else \
                                                                        PROFILE_MAP[ENTREPRENUER_PROFILE_NAME])
        return context

    def get_template_names(self, *ar, **kw):
        template_name = profile = get_profile({'user__id': self.request.user.id})
        template_name = 'common/mentor_profile.html' if profile.is_mentor else 'common/entreprenuer_profile.html'
        return [template_name]


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
    #form_class = EntrepreneurProfileEditForm
    template_name = 'common/edit_profile.html'

    @method_decorator(login_required)
    def dispatch(self, request, *ar, **kw):
        return super(EditProfileView, self).dispatch(request, *ar, **kw)

    """def get_form_class(self, *args, **kwargs):

        print(form_class, "form_class")
        return form_class"""

    def get_context_data(self, *args, **kwargs):
        context = super(EditProfileView, self).get_context_data(*args, **kwargs)
        #initial = self.initial
        #pk = self.kwargs['pk']
        is_mentor = True
        profile = get_profile({'user__id':self.request.user.id})

        #experience_formset = modelformset_factory(Experience, form=ExperienceForm, extra=1)
        #experience_formset = experience_formset(queryset=profile.experience.all())
        #print(experience_formset, "EF")
        context.update(profile_type=self.kwargs['profile_type'])
                       #experience_formset=experience_formset)
        print(context, "Context")
        return context

    def get_initial(self):
        print("INITIAL")
        profile = get_profile({'user__id':self.request.user.id})
        mentor = profile.mentor
        entreprenuer = profile.entreprenuer
        initial_dict = {}
        profile_type = self.kwargs['profile_type']

        if profile_type == MENTOR_PROFILE_NAME:
            if mentor:
                mentor_attributes = ['management_experience', 'ownership_experience', 'business_experience_country',
                                     'website', 'company', 'company_role', 'professional_experience']
                initial_dict.update(industry=mentor.industry.all(),
                                    expert_areas=mentor.expert_areas.all())
                for i in mentor_attributes:
                    print(i, mentor.management_experience, )
                    initial_dict.update({i: mentor.__getattribute__(i)})
        elif profile_type == ENTREPRENUER_PROFILE_NAME:
            if entreprenuer:
                ent_attributes = ['experience', 'professional_experience', 'need_help']
                initial_dict.update(industry=entreprenuer.industry.all(),
                                    expert_areas=entreprenuer.expert_areas.all())
                for i in ent_attributes:
                    initial_dict.update({i: entreprenuer.__getattribute__(i)})
        print(initial_dict)
        return  initial_dict


    def get_form(self):
        print(self.form_class)
        #instance = Profile.objects.get(id=pk)
        profile_type = self.kwargs['profile_type']
        profile = get_profile({'user__id': self.request.user.id})
        if profile_type == MENTOR_PROFILE_NAME:
            form_class = MentorProfileEditForm
        else:
            form_class = EntrepreneurProfileEditForm
        return form_class(instance=profile, **self.get_form_kwargs())

    def form_valid(self, form):
        print(self.request.POST, self.request.FILES)
        data = form.cleaned_data
        first_name = form.cleaned_data['first_name'].title()
        last_name = form.cleaned_data['last_name'].title()
        form = form.save(commit=False)
        form.user.first_name = first_name
        form.user.last_name = last_name
        form.user.save()
        form.save()
        profile = get_profile({'user__id': self.request.user.id})
        print(data)
        profile_type = self.kwargs['profile_type']
        if profile_type == MENTOR_PROFILE_NAME:
            if not profile.mentor:
                mentor = MentorProfile(professional_experience=data['professional_experience'],
                              management_experience=data['management_experience'],
                              ownership_experience=data['ownership_experience'],
                              business_experience_country=data['business_experience_country'],
                              website=data['website'],
                              company=data['company'],
                              company_role=data['company_role'])
                mentor.save()
                for i in data['industry']:
                    mentor.industry.add(i)
                profile.mentor = mentor
                profile.save()
            else:
                mentor = profile.mentor
                mentor.professional_experience = data['professional_experience']
                mentor.management_experience = data['management_experience']
                mentor.ownership_experience = data['ownership_experience']
                mentor.business_experience_country = data['business_experience_country']
                mentor.website = data['website']
                mentor.company = data['company']
                mentor.company_role = data['company_role']
                mentor.industry = data['industry']
                profile.mentor = mentor
                profile.mentor.save()

        elif not profile.entreprenuer:
            ent = EntrepreneurProfile(professional_experience=data['professional_experience'],
                                        need_help=data['need_help'])
            ent.save()
            for i in data['industry']:
                ent.industry.add(i)
            profile.entreprenuer = ent
            profile.save()
        else:
            ent = profile.entreprenuer
            ent.professional_experience = data['professional_experience']
            ent.industry = data['industry']
            ent.need_help = data['need_help']
            ent.save()
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
        results = []
        print(get_dict)
        if self.kwargs['whom'] == 'group':
            self.template_name = 'common/search_group.html'
        elif self.kwargs['whom'] in ['mentor', 'entrepreneur']:
            self.template_name = 'common/search_profile.html'
            #print(self.template_name)
        if self.kwargs['whom'] == 'group':
            results = Group.objects.all()
            if 'keywords' in get_dict and get_dict['keywords']:
                results = results.filter(Q(title__icontains=get_dict['keywords']) | Q(description__icontains=get_dict['keywords']))
        elif self.kwargs['whom'] == 'mentor':
            results = Profile.objects.filter(is_mentor=True)
            if 'industry' in get_dict and get_dict['industry']:
                results = results.filter(mentor__industry__name__icontains=get_dict['industry'])
        elif self.kwargs['whom'] == 'entrepreneur':
            results = Profile.objects.filter(is_mentor=False)
            if 'industry' in get_dict and get_dict['industry']:
                results = results.filter(entreprenuer__industry__name__icontains=get_dict['industry'])
        #if 'industry' in get_dict and get_dict['industry']:
        #    results = results.filter(industry__name__icontains=get_dict['industry'])
        if 'country' in get_dict and get_dict['country']:
            results = results.filter(country=get_dict['country'])
        if 'languages_spoken' in get_dict and get_dict['languages_spoken']:
            results = results.filter(languages_spoken__name__icontains=get_dict['languages_spoken'])
        if 'keywords' in get_dict and get_dict['keywords']:
            results = results.filter(Q(user__first_name__icontains=get_dict['keywords']) | Q(user__last_name__icontains=get_dict['keywords']))
        context.update(results=results,
                       search=self.kwargs['whom'].title())
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
    model = Group
    template_name = 'common/group-detail.html'
    fields = ('id',)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GroupDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(GroupDetailView, self).get_context_data(*args, **kwargs)
        current_user = self.request.user
        #profile = get_profile({'user__id': current_user.id})
        if self.object.members.filter(user__id=current_user.id).exists():
            context.update(is_joined=True)
        if self.object.created_by.id == current_user.id:
            context.update(is_owner=True)
        #question_answers = GroupConversationIntermediate
        members = self.object.members.all()
        print(members, "MEM")
        print(members.filter(is_mentor=True))
        print(members.filter(is_mentor=False))
        #print(context, self.object.owner_id,current_user.id, current_user.id )
        context.update(mentor_group=members.filter(is_mentor=True),
                       entrepreneur_group=members.filter(is_mentor=False))
        return context

    def post(self, *args, **kwargs):
        current_user = self.request.user
        #print(dir(self))
        member_profile = get_profile({'user__id': current_user.id})
        self.get_object().members.add(member_profile)
        #self.object.save()
        #print(self.request.user)
        messages.success(self.request, "You have joined this group successfully!")
        return HttpResponseRedirect(reverse('group-detail', kwargs={'pk': self.kwargs['pk']}))

class TrainingDetailView(DetailView):
    model = Course
    template_name = 'common/group-training-detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TrainingDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(TrainingDetailView, self).get_context_data(*args, **kwargs)
        current_user = self.request.user
        context.update(current_user=current_user,
                       current_user_profile=get_profile(user__id=current_user.id),
                       messages=self.object.messages.all().order_by('id'))
        print(context, self.object.owner_id, current_user.id, current_user.id)
        return context

class CreateCourseView(FormView):
    template_name = 'create_course.html'

    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateCourseView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(CreateCourseView, self).get_context_data(*args, **kwargs)
        return context

    def form_valid(self, form):
        new_course = form.save(commit=False)
        new_course.save()
        messages.success(self.request, "You have created the course successfully!")
        return HttpResponseRedirect(reverse('course-list'))

class CourseListingView(View):
    template_name = 'common/course_listing.html'

    def get(self, request, * args, **kwargs):
        context = {}
        search_data = self.request.GET
        courses = Course.objects.all()
        teachers = {}
        result = []
        json_response = []
        profiles = Profile.objects.filter(course_teachers__isnull=False)
        for i in profiles:
            name = '%s %s' % (i.user.first_name.title(), i.user.last_name.title())
            if name not in teachers:
                teachers[name] = 1
            else:
                teachers[name] += 1

        if ('category' in search_data and search_data['category']):
            courses = courses.filter(category__icontains=search_data['category'])
        print(search_data, "SEARCH DATA!", courses)

        if self.request.is_ajax():
            if 'teacher' in search_data:
                #print(search_data['teacher'], "TE")
                for t in search_data.getlist('teacher'):
                    first_name, last_name = t.split(' ', 1) if t.find(' ') >= 0 else [t, '']
                    course = courses.filter(teacher__user__first_name__icontains=first_name,
                                            teacher__user__last_name__icontains=last_name).\
                                             values_list('id', flat=True)
                    result.extend(course)

            courses = courses.filter(id__in=set(result))

            if 'offer' in search_data:
                for o in search_data.getlist('offer'):
                    print(o, int(o), "OFFERWW")
                    course = courses.filter(offer__gte=int(o)).values_list('id', flat=True)
                    print(course, "OFFFER")
                    result.extend(course)

            courses = courses.filter(id__in=set(result))

            if 'rating' in search_data:
                rating = int(search_data['rating'])
                #print(rating, "rating")
                course = courses.filter(rating__gte=rating).values_list('id', flat=True)
                result.extend(course)

            courses = courses.filter(id__in=set(result))
            json_response = render_to_string('common/includes/course_mid_listing.html', {'courses': courses})
            return JsonResponse({'result': json_response})

        print(teachers, "TEACHERS")
        context.update(courses=courses,
                       teachers=teachers)
        return render(self.request, self.template_name, context)


class AddGroupConversation(View):

    def post(self, request, *args, **kwargs):
        group_id = self.kwargs['group']
        group = Group.objects.get(id=group_id)
        members = group.memebers.all()
        data = self.request.POST
        print(data)

        conversation = Conversation(sender=request.user,
                                    message=data['message'],
                                    message_type=GROUP_MESSAGE)
        conversation.save()
        group_conversation = GroupConversationIntermediate(conversation=conversation,
                                      group=group)
        if 'is_question' in data:
            group_conversation.is_question = True
        group_conversation.save()

        return JsonResponse({'result': 'success'})

class CourseDetailView(View):
    template_name = 'common/course-detail.html'

    def get(self, request, *args, **kwargs):
        object = Course.objects.get(id=self.kwargs['pk'])
        is_purchased = True if self.request.user.is_authenticated() and \
                               Payment.objects.filter(buyer__user__id=self.request.user.id,
                                                      course__id=self.kwargs['pk']).exists() else False
        context = {'object': object,
                   'is_purchased': is_purchased}
        return render(self.request, self.template_name, context)

    """def post(self, *args, **kwargs):
        current_user = self.request.user
        #print(dir(self))
        member_profile = get_profile({'user__id': current_user.id})
        self.get_object().members.add(member_profile)
        #self.object.save()
        #print(self.request.user)
        messages.success(self.request, "You have joined this group successfully!")
        return HttpResponseRedirect(reverse('group-detail', kwargs={'pk': self.kwargs['pk']}))"""

class CoursePayView(View):
    template_name = 'common/payment.html'


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CoursePayView, self).dispatch(*args, **kwargs)


    def get(self, request, *args, **kwargs):
        course = Course.objects.get(id=self.kwargs['pk'])
        context = {'course': course}
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        response = requests.get("%s%s" %(settings.PAYSTACK_API_URL, self.request.POST['reference']), headers={'Authorization' : 'Bearer %s' % settings.PAYSTACK_API_SECRET_KEY})
        response = response.json()
        if response['status']:
            payment = Payment(buyer=get_profile({'user__id': self.request.user.id}),
                              course=Course.objects.get(id=self.kwargs['pk']),
                              reference=self.request.POST['reference'],
                              status=response['data']['status'],
                              reason=response['message'])
            payment.save()
            messages.success(self.request, "Your amount has been successfully transferred!")
        return JsonResponse({'result': 'success'})

class GroupConversationView(View):
    template_name = 'common/group_conversations.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GroupConversationView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        group = Group.objects.get(id=self.kwargs['pk'])
        context = {'group': group}
        conversation_comments = []
        conversations = group.messages.filter(parent__isnull=True).order_by('-id')
        for c in conversations:
            conversation_comments.append({'comments': Conversation.objects.filter(parent=c).order_by('-id'),
                                          'conversation': c})
        context.update(conversation_comments=conversation_comments)
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        post_data = self.request.POST
        group = Group.objects.get(id=self.kwargs['pk'])
        conversation = Conversation(from_user=self.request.user,
                                    message=post_data['new_post'])
        conversation.save()
        GroupConversationIntermediate(group=group,
                                      conversation=conversation).save()
        new_post = render_to_string('common/includes/group-inline-conversation.html', {'message': conversation})
        return JsonResponse({'result': 'success',
                             'new_post': new_post})

class CommentConversationView(View):
    def post(self, request, *args, **kwargs):
        print(self.request.POST)
        post_data = self.request.POST
        parent_conversation = Conversation.objects.get(id=self.kwargs['pk'])
        conversation = Conversation(from_user=self.request.user,
                                    message=post_data['new_post'],
                                    parent=parent_conversation)
        conversation.save()
        new_comment = render_to_string('common/includes/group-conversation-comment.html', {'comment': conversation})
        return JsonResponse({'result': 'success',
                             'new_comment': new_comment})