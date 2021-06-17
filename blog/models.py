from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # timezone.now sets time of post and can be updated if necessary
    date_posted = models.DateTimeField(default=timezone.now)
    # set up many to one relationship (many posts to one author)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """return url to detail view as string
        after post creation/modification"""
        return reverse('post-detail', kwargs={'pk': self.pk})
