from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    remember_me = forms.BooleanField(label='Remember Me', required=False)
