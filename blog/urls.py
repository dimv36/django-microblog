from django.urls import path

from . import views
from .views import EditProfileView

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('user/<str:username>', views.user, name='user'),
    path('edit_profile', EditProfileView.as_view(), name='edit_profile'),
    path('follow/<str:username>', views.follow, name='follow'),
    path('unfollow/<str:username>', views.unfollow, name='unfollow'),
]
