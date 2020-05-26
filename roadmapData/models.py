from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.CharField(max_length=255, default='')
    username = models.CharField(max_length=255, unique=True, default='')
    password = models.CharField(max_length=255, default='')
    interest = models.TextField(blank=True, default='')


class Article(models.Model):
    article_references = models.ManyToManyField("self", blank=True, symmetrical=False)

    title = models.CharField(max_length=200, blank=True, default='')
    alias = models.CharField(max_length=200, blank=True, default='')
    author = models.TextField(blank=True, default='')
    journal = models.CharField(max_length=200, blank=True, default='')
    volume = models.IntegerField(blank=True, default=0)
    pages = models.IntegerField(blank=True, default=0)
    years = models.IntegerField(blank=True, default=0)
    url = models.CharField(max_length=500, blank=True, default="")
    bibtext = models.TextField(blank=True, default='')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_state = models.BooleanField(blank=True, default=False)
    note = models.TextField(blank=True, default='')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, default='')


class Essay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.ManyToManyField(Comment, blank=True)

    title = models.CharField(max_length=200, blank=True, default='')
    text = models.TextField(blank=True, default='')


class RoadMap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    road_maps = models.ManyToManyField("self", blank=True, symmetrical=False)
    articles = models.ManyToManyField(Article, blank=True)
    essays = models.ManyToManyField(Essay, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)

    title = models.CharField(max_length=200, blank=True, default='')
    text = models.TextField(blank=True, default='')
    description = models.TextField(blank=True, default='')


class RoadMapShareId(models.Model):
    roadmap = models.ForeignKey(RoadMap, on_delete=models.CASCADE)
    sha256 = models.CharField(max_length=64)


class Feedback(models.Model):
    text = models.TextField(default='')


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, default='')

    essays = models.ManyToManyField(Essay, blank=True)
    roadmaps = models.ManyToManyField(RoadMap, blank=True)
    articles = models.ManyToManyField(Article, blank=True)


class Term(models.Model):
    name = models.TextField(blank=True, default='')


class Newpaper(models.Model):
    term = models.ManyToManyField(Term, blank=True)
    text = models.TextField(blank=True, default='')
