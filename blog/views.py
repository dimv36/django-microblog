from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from .models import *
from .forms import LoginForm, RegistrationForm, EditProfileForm, PostSendForm

# Create your views here.


@login_required
def index(request):
    form = PostSendForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST':
        if form.is_valid():
            post = Post(body=form.data.get('body'), user=request.user)
            post.save()
            messages.info(request, _('Your post added!'))
            return redirect('index')
    page = request.GET.get('page', 1)
    post_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(post_list, settings.POSTS_PER_PAGE)
    posts = paginator.get_page(page)
    context = {'posts': posts, 'title': _('Home'), 'form': form}
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
                messages.success(request, _('Logged as {}').format(form.data.get('username')))
                return HttpResponseRedirect('index')
            else:
                messages.error(request, _('Login failed for user {}').format(form.data.get('username')))
    return render(request, 'login.html', context={'title': _('Sign In'),
                                                  'form': form})


def signup(request):
    form = RegistrationForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, _('User {} successfully created!').format(username))
            return HttpResponseRedirect('login')
    return render(request, 'registration.html', {'form': form, 'title': _('Sign up')})


def logout(request):
    django_logout(request)
    return HttpResponseRedirect('index')


@login_required
def user(request, username):
    user = get_object_or_404(Author, username=username)
    page = request.GET.get('page', 1)
    post_list = user.post_set.order_by('-timestamp')
    paginator = Paginator(post_list, settings.POSTS_PER_PAGE)
    posts = paginator.get_page(page)
    return render(request, 'user.html', context={'user': user,
                                                 'posts': posts,
                                                 'title': _('User {}').format(username),
                                                 'current_is_following': request.user.is_following(user)})


class EditProfileView(View):
    def get(self, request):
        form = EditProfileForm(instance=request.user)
        context = {'title': _('Edit profile'), 'form': form}
        return render(request, 'edit_profile.html', context)

    def post(self, request):
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your changes have been saved.'))
        else:
            messages.error(request, 'Form invalid!')
        return HttpResponseRedirect('edit_profile')


@login_required
def follow(request, username):
    user = Author.objects.filter(username=username).first()
    if user is None:
        messages.error(request, _('User {} not found.').format(username))
        return redirect('index')
    if user == request.user:
        messages.error(_('You cannot follow yourself!'))
        return redirect('user', username=username)
    request.user.follow(user)
    messages.success(request, _('You are following {}!').format(username))
    return redirect('user', username=username)


@login_required
def unfollow(request, username):
    user = Author.objects.filter(username=username).first()
    if user is None:
        messages.error(request, _('User {} not found.').format(username))
        return redirect('index')
    if user == request.user:
        messages.error(_('You cannot unfollow yourself!'))
        return redirect('user', username=username)
    request.user.unfollow(user)
    messages.success(request, _('You are not following {}.').format(username))
    return redirect('user', username=username)


@login_required
def posts(request):
    page = request.GET.get('page', 1)
    post_list = Post.objects.order_by('-timestamp')
    paginator = Paginator(post_list, settings.POSTS_PER_PAGE)
    posts = paginator.get_page(page)
    context = {'posts': posts, 'title': _('All posts')}
    return render(request, 'index.html', context)
