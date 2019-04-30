from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from .forms import LoginForm

# Create your views here.


def index(request):
    user = {'username': 'testuser'}
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
    context = {'user': user,
               'posts': posts}
    return render(request, 'index.html', context)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Login requested for user {}, remember_me={}'.format(
                form.data.get('username'), form.data.get('remember_me')))
            return HttpResponseRedirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', context={'title': 'Sign In',
                                                  'form': form})
