from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Author


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


class RegistrationForm(UserCreationForm):
    about_me = forms.CharField(label='Description', required=False, widget=forms.Textarea(),
                               help_text='Optional')
    email = forms.EmailField(label='Email address')

    class Meta:
        model = Author
        fields = ('username', 'email', 'about_me')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and Author.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email addresses must be unique.')
        return email


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('username', 'about_me')


class PostSendForm(forms.Form):
    body = forms.CharField(label='Message', widget=forms.Textarea())
