from django.http import HttpResponse
from django.shortcuts import render

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
