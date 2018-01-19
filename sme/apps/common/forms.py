'''
Initialize forms here!
'''

from django import forms
from django.contrib.auth.models import User
from datetime import date

from .models import (Profile, EntrepreneurProfile, MentorProfile,
                     Industry, Languages, Experience,
                     Conversation, Course, Group, COUNTRY_CHOICES, GENDER_CHOICES,
                     BIRTH_YEAR_CHOICES)

PROFILE_TYPE_CHOICES = [
    ('', '-- Select --'),
    ('entrepreneur', 'entrepreneur'),
    ('mentor', 'Mentor')
]

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
cur_year = date.today().year
EXPERIENCE_MONTH_CHOICES = [(index + 1, month_val) for index, month_val in enumerate(MONTHS)]
EXPERIENCE_YEAR_CHOICES = [(year_val, year_val) for year_val in reversed(range(cur_year - 50, cur_year + 1))]
INDUSTRY_CHOICES = [(val, val) for val in Industry.objects.all().values_list('name', flat=True)]
INDUSTRY_CHOICES.insert(0, ('', '-- Select --'))
LANGUAGES_CHOICES = [(val, val) for val in Languages.objects.all().values_list('name', flat=True).distinct()]
LANGUAGES_CHOICES.insert(0, ('', '-- Select --'))

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30,
                                 widget=forms.TextInput(attrs={"class": "form-control",
                                                               "placeholder": "First name",
                                                               "required": "",
                                                               "autofocus": ""}))
    last_name = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs={"class": "form-control",
                                                              "placeholder": "Last name",
                                                              "required": ""}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control",
                                                           "placeholder": "Email address",
                                                           "required": ""}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={"class": "form-control",
                                                                                "placeholder": "Password",
                                                                                "required": ""}))
    confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={"class": "form-control",
                                                                                        "placeholder": "Confirm Password",
                                                                                        "required": ""}))
    profile_type = forms.ChoiceField(widget=forms.RadioSelect(attrs={"class": "form-control",
                                                                "required": ""},
                                                        ),
                                     choices=PROFILE_TYPE_CHOICES)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__icontains=email.strip()).exists():
           raise forms.ValidationError("Email already exists!")
        return email

    def save(self):
        data = self.cleaned_data
        user = User(first_name=data['first_name'].strip(),
                    last_name=data['last_name'].strip(),
                    email=data['email'].strip(),
                    username=data['email'].strip())
        user.set_password(data['password'])
        user.save()
        profile_type = data['profile_type']
        profile = Profile.objects.create(user=user)
        if profile_type == 'mentor':
            profile.is_mentor = True
            profile.save()
        return profile

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError("Passwords didn't match!")
        return confirm_password

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30,
                                 widget=forms.TextInput(attrs={"class": "form-control",
                                                               "placeholder": "First name",
                                                               "required": "",
                                                               "autofocus": ""}))
    last_name = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs={"class": "form-control",
                                                              "placeholder": "Last name",
                                                              "required": ""}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                             "placeholder": "Address",
                                                             "required": ""}))
    city = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs={"class": "form-control",
                                                              "placeholder": "City",
                                                              "required": ""}))
    state = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs={"class": "form-control",
                                                              "placeholder": "State",
                                                              "required": ""}))
    country = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control",
                                                           "required": ""}),
                                choices=COUNTRY_CHOICES)
    about_me = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
                               help_text="About yourself to know more!")
    industry = forms.ModelMultipleChoiceField(queryset=Industry.objects.all(),
                                              widget=forms.SelectMultiple(attrs={"class": "form-control",
                                                                                 "required": "",
                                                                                 "data-placeholder": "Select Industry"}),
                                              help_text='Your industry!')
    languages_spoken = forms.ModelMultipleChoiceField(queryset=Languages.objects.all(),
                                               widget=forms.SelectMultiple(attrs={"class": "form-control",
                                                                                  "data-placeholder": "Select Language"}),
                                                      help_text='Speak, Write and Read languages!')
    postal_code = forms.CharField(max_length=6,
                              widget=forms.TextInput(attrs={"class": "form-control",
                                                            "placeholder": "",
                                                            "required": ""}))
    phone_number = forms.CharField(max_length=20,
                              widget=forms.TextInput(attrs={"class": "form-control",
                                                            "placeholder": "",
                                                            }),
                               help_text='123-456-7890 x123')
    gender = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),
                                choices=GENDER_CHOICES)
    birth_year = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),
                               choices=BIRTH_YEAR_CHOICES)
    photo = forms.ImageField(widget=forms.FileInput(attrs={"width": 98,
                                                           "height": 98}),
                             required=False)
    #professional_experience = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['first_name'].initial = kwargs['instance'].user.first_name
            self.fields['last_name'].initial = kwargs['instance'].user.last_name

    class Meta:
        model = Profile
        exclude = ('user', 'agree_terms', 'is_mentor')

class EntrepreneurProfileEditForm(ProfileForm):
    professional_experience = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    need_help = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, "required":""}),
                                required=False,
                                help_text='(What do you need to know?)')

    """class Meta:
        model = EntrepreneurProfile
        exclude = ('user',)"""

class MentorProfileEditForm(ProfileForm):
    professional_experience = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
                                              help_text='(What roles have you played in your career and how did you contribute? What experiences would you like to share in a mentoring connection? What accomplishments are you proud of?)')
    business_experience_country = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control width-200 d-i-b ver-align-m"}),
                                                    choices=COUNTRY_CHOICES)
    company = forms.CharField(max_length=100,
                              widget=forms.TextInput(attrs={"class": "form-control",
                                                            "placeholder": ""}))
    company_role = forms.CharField(max_length=30,
                                   widget=forms.TextInput(attrs={"class": "form-control",
                                                                 "placeholder": "Role..."}))
    management_experience = forms.IntegerField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                             "placeholder": ""}))
    ownership_experience = forms.IntegerField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                            "placeholder": ""}))
    website = forms.URLField(widget=forms.TextInput(attrs={"class": "form-control",
                                                           "placeholder": ""}),
                             help_text="This could be your website, or alternately the address of your portfolio, professional bio, blog, or LinkedIn profile.")

    """class Meta:
        model = MentorProfile
        exclude = ('user',)"""

class ExperienceForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control width-200 d-i-b ver-align-m",
                                                            "placeholder": "Name",
                                                            "required": ""}))
    country = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control width-200 d-i-b ver-align-m",
                                                           "required": ""}),
                                choices=COUNTRY_CHOICES)
    start_month = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control width-200 d-i-b ver-align-m",
                                                           "required": ""}),
                                choices=EXPERIENCE_MONTH_CHOICES)
    start_year = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control width-200 d-i-b ver-align-m",
                                                           "required": ""}),
                                choices=EXPERIENCE_YEAR_CHOICES)
    end_month = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control width-200 d-i-b ver-align-m",
                                                           "required": ""}),
                                choices=EXPERIENCE_MONTH_CHOICES)
    end_year = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control width-200 d-i-b ver-align-m",
                                                           "required": ""}),
                                choices=EXPERIENCE_YEAR_CHOICES)
    industry = forms.ModelMultipleChoiceField(queryset=Industry.objects.all(),
                                              widget=forms.SelectMultiple(attrs={"class": "form-control width-200 d-i-b ver-align-m",
                                                                                 "required": ""}))
    url = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control width-200 d-i-b ver-align-m",
                                                            "placeholder": "Website URL",
                                                            "required": ""}))

    class Meta:
        model = Experience
        exclude = ('created_at',)

class ConversationForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'cols': 40,
                                                           'placeholder': "Write a nice message"}))

    class Meta:
        model = Conversation
        exclude = ('created_at', 'from_user', 'to_user', 'message_type')

class SearchForm(forms.Form):
    industry = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),
                                 choices=INDUSTRY_CHOICES,
                                 required=False)
    country = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),
                                 choices=COUNTRY_CHOICES, required=False)
    languages_spoken = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),
                                    choices=LANGUAGES_CHOICES,
                                         required=False)
    keywords = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                            "placeholder": "Special keywords"}),
                               required=False)


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        exclude = ('owner', )

class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        exclude = ('created_by', )