from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Author(AbstractUser):
    about_me = models.TextField('About me', max_length=140, null=True)

    def follow(self, user):
        if not self.is_following(user):
            self.following.add(Follower(following=user), bulk=False)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.filter(following=user).delete()

    def is_following(self, user):
        return self.following.filter(following=user).count() > 0

    def followed_posts(self):
        return Post.objects.filter(user_id__in=self.following.values('following_id')).order_by('-timestamp')


class Post(models.Model):
    body = models.TextField('Post text', max_length=140)
    timestamp = models.DateTimeField(db_index=True, auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __repr__(self):
        return '<Post: {} author: {}>'.format(self.body, self.user.username)


class Follower(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return '<{} follows {}>'.format(self.follower, self.following)
