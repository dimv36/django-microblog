from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Author


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput())


class RegistrationForm(UserCreationForm):
    about_me = forms.CharField(label=_('Description'), required=False, widget=forms.Textarea(),
                               help_text=_('Optional'))
    email = forms.EmailField(label=_('Email address'))

    class Meta:
        model = Author
        fields = ('username', 'email', 'about_me')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and Author.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(_('Email addresses must be unique.'))
        return email


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('username', 'about_me')


class PostSendForm(forms.Form):
    body = forms.CharField(label=_('Message'), widget=forms.Textarea())
