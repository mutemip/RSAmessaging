from django import forms
from django.contrib.auth import authenticate
from .models import *


class UserRegistrationForm(forms.ModelForm):
    firstname = forms.CharField(widget=forms.TextInput(attrs={'size': 30, 'placeholder': 'Enter Your Name'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={'size': 30, 'placeholder': 'Enter Your Name'}))
    public_key = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Paste your Public Key'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'size': 30, 'placeholder': 'Type your password'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'size': 30, 'placeholder': 'Enter Email Address'}))

    class Meta:
        model = CustomeUser
        fields = ('firstname', 'lastname', 'email', 'public_key', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = CustomeUser.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('Email is already been used')
        return email


class MessagesForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(queryset=CustomeUser.objects.all(), empty_label=None)
    Message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Messages
        fields = ('receiver', 'Message')


class LoginFormAuth(forms.Form):
    username = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('The user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(LoginFormAuth, self).clean(*args, **kwargs)
