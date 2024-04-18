from datetime import datetime
from datetime import date

import logging
logger = logging.getLogger(__name__)

from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class LoginEmailForm(forms.Form):
    email = forms.EmailField(label="email", max_length=180)
    password = forms.CharField(label="password", max_length=200, widget=forms.PasswordInput)

    def __str__(self):
        return f"Login form for user with email '{self.cleaned_data['email']}'"

class LoginUserForm(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(label="password", max_length=200, widget=forms.PasswordInput)
    
    def __str__(self):
        return f"Login form for user '{self.cleaned_data['username']}'"

class RegistrationForm(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    email = forms.EmailField(label="email", max_length=180)
    repeated_email = forms.EmailField(label="repeated_email", max_length=180)
    password = forms.CharField(label="password", max_length=200, widget=forms.PasswordInput)
    repeated_password = forms.CharField(label="repeated_password", max_length=200, widget=forms.PasswordInput)
    
    def __str__(self):
        return f"Registration form for user '{self.cleaned_data['username']}' and email '{self.cleaned_data['email']}'"

    def clean(self):
        self.cleaned_data = super().clean()
        
        missing_fields = False
        username = self.cleaned_data.get('username', None)
        if not username:
            missing_fields = True
            self.add_error('username', 'username must be included.')

        email = self.cleaned_data.get('email', None)
        if not email:
            missing_fields = True
            self.add_error('email', 'Email must be included.')

        rep_email = self.cleaned_data.get('repeated_email', None)
        if not rep_email:
            missing_fields = True
            self.add_error('repeated_email', 'Repeated email must be included.')

        psw = self.cleaned_data.get('password', None)
        if not psw:
            missing_fields = True
            self.add_error('password', 'Password must be included.')

        rep_psw = self.cleaned_data.get('repeated_password', None)
        if not rep_psw:
            missing_fields = True
            self.add_error('repeated_password', 'Repeated password must be included.')

        if missing_fields:
            return self.cleaned_data

        if psw != rep_psw:
            self.add_error('password', 'Password and repeated password must match.')
        
        if email != rep_email:
            self.add_error('email', 'Email and repeated email must match.')

        try:
            validate_password(psw)
        except ValidationError as e:
            self.add_error('password', e)

        return self.cleaned_data
    
class EmailForm(forms.Form): 
    email = forms.EmailField(label="email", max_length=180)

    def __str__(self):
        return f"Email recovery form for '{self.cleaned_data['email']}'"


class PasswordResetForm(forms.Form):
    password = forms.PasswordInput()
    repeated_password = forms.PasswordInput()

    def __str__(self):
        return f"Password reset form"
