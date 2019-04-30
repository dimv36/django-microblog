from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.shortcuts import render
from django.contrib import messages
from .models import *
from .forms import LoginForm, RegistrationForm

# Create your views here.


@login_required
def index(request):
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    context = {'posts': posts}
    return render(request, 'index.html', context)


def login(request):
    form = LoginForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.data.get('username')
            raw_password = form.data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user:
                django_login(request, user)
                messages.success(request, 'Logged as {}'.format(form.data.get('username')))
                return HttpResponseRedirect('index')
            else:
                messages.error(request, 'Login failed for user {}'.format(form.data.get('username')))
    return render(request, 'login.html', context={'title': 'Sign In',
                                                  'form': form})


def signup(request):
    form = RegistrationForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'User {} successfully created!'.format(username))
            return HttpResponseRedirect('login')
    return render(request, 'registration.html', {'form': form})


def logout(request):
    django_logout(request)
    return HttpResponseRedirect('index')
