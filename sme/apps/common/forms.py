'''
Initialize forms here!
'''

from django import forms

from django.contrib.auth.models import User

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
        return user

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError("Passwords didn't match!")
        return confirm_password
