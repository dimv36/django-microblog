from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Author(AbstractUser):
    pass


class Post(models.Model):
    body = models.TextField('Post text', max_length=140)
    timestamp = models.DateTimeField(db_index=True, auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __repr__(self):
        return '<Post: {} author: {}>'.format(self.body, self.user.username)
