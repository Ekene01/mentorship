'''
Initialize forms here!
'''

from django import forms
from django.contrib.auth.models import User
from datetime import date

from .models import (EntrepreneurProfile, MentorProfile,
                     Industry, Languages, Experience,
                     COUNTRY_CHOICES)

PROFILE_TYPE_CHOICES = [
    ('', '-- Select --'),
    ('entrepreneur', 'entrepreneur'),
    ('mentor', 'Mentor')
]

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
cur_year = date.today().year
EXPERIENCE_MONTH_CHOICES = [(month_val, month_val) for month_val in enumerate(MONTHS)]
EXPERIENCE_YEAR_CHOICES = [(year_val, year_val) for year_val in reversed(range(cur_year - 50, cur_year + 1))]

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
    profile_type = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control",
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
        if profile_type == 'mentor':
            MentorProfile.objects.create(user=user)
        else:
            EntrepreneurProfile.objects.create(user=user)
        return user

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
                                                              "placeholder": "Last name",
                                                              "required": ""}))
    state = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs={"class": "form-control",
                                                              "placeholder": "Last name",
                                                              "required": ""}))
    country = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control",
                                                           "required": ""}),
                                choices=COUNTRY_CHOICES)
    about_me = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    industry = forms.ModelMultipleChoiceField(queryset=Industry.objects.all(),
                                              widget=forms.SelectMultiple(attrs={"class": "form-control",
                                                                                 "required": ""}))
    languages_spoken = forms.ModelMultipleChoiceField(queryset=Languages.objects.all(),
                                               widget=forms.SelectMultiple(attrs={"class": "form-control",
                                                                                  }))
    photo = forms.ImageField(widget=forms.FileInput(attrs={"width": 98,
                                                           "height": 98}),
                             required=False)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['first_name'].initial = kwargs['instance'].user.first_name
            self.fields['last_name'].initial = kwargs['instance'].user.last_name

class EntrepreneurProfileEditForm(ProfileForm):
    professional_experience = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    class Meta:
        model = EntrepreneurProfile
        exclude = ('user',)

class MentorProfileEditForm(ProfileForm):
    professional_experience = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    class Meta:
        model = MentorProfile
        exclude = ('user',)

class ExperienceForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                            "placeholder": "Address",
                                                            "required": ""}))
    country = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control",
                                                           "required": ""}),
                                choices=COUNTRY_CHOICES)
    start_month = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control",
                                                           "required": ""}),
                                choices=EXPERIENCE_MONTH_CHOICES)
    start_year = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control",
                                                           "required": ""}),
                                choices=EXPERIENCE_MONTH_CHOICES)
    end_month = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control",
                                                           "required": ""}),
                                choices=EXPERIENCE_MONTH_CHOICES)
    end_year = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control",
                                                           "required": ""}),
                                choices=EXPERIENCE_MONTH_CHOICES)
    industry = forms.ModelMultipleChoiceField(queryset=Industry.objects.all(),
                                              widget=forms.SelectMultiple(attrs={"class": "form-control",
                                                                                 "required": ""}))
    url = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                            "placeholder": "Website URL",
                                                            "required": ""}))

    class Meta:
        model = Experience
        exclude = ('created_at',)