from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=200, blank=True, default='')
    author = models.CharField(max_length=200, blank=True, default='')
    journal = models.CharField(max_length=200, blank=True, default='')
    volume = models.IntegerField()
    pages = models.IntegerField()
    years = models.IntegerField()
    url = models.URLField(max_length=200, default="")
