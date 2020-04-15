from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=200, blank=True, default='')
    author = models.CharField(max_length=200, blank=True, default='')
    journal = models.CharField(max_length=200, blank=True, default='')
    volume = models.IntegerField(blank=True, default=0)
    pages = models.IntegerField(blank=True, default=0)
    years = models.IntegerField(blank=True, default=0)
    url = models.URLField(max_length=200, default="")


class Essay(models.Model):
    text = models.TextField(blank=True, default='')


class RoadMap(models.Model):
    text = models.TextField(blank=True, default='')
