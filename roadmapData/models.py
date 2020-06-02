from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.CharField(max_length=255, default='')
    username = models.CharField(max_length=255, unique=True, default='')
    password = models.CharField(max_length=255, default='')
    interest = models.TextField(blank=True, default='')
    city = models.CharField(max_length=300, default='')
    organization = models.CharField(max_length=300, default='')
    bio = models.CharField(max_length=300, default='')


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, default='')


class Article(models.Model):
    READ_STATE_CHOICES = (('U', 'unread'),
                          ('I', 'reading'),
                          ('F', 'read'))

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
    article_references = models.ManyToManyField("self", blank=True, symmetrical=False)
    read_state = models.CharField(max_length=1, choices=READ_STATE_CHOICES, default='U')
    note = models.TextField(blank=True, default='')
    tag = models.ManyToManyField(Tag, blank=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, default='')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, default='')


class Essay(models.Model):
    STATE_CHOICES = (('U', 'unfinished'),
                     ('I', 'writing'),
                     ('F', 'finished'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200, blank=True, default='')
    author = models.CharField(max_length=200, blank=True, default='')
    abstract = models.TextField(blank=True, default='')
    text = models.TextField(blank=True, default='')
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='U')
    tag = models.ManyToManyField(Tag, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    comment = models.ManyToManyField(Comment, blank=True)


class RoadMap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    road_maps = models.ManyToManyField("self", blank=True, symmetrical=False)
    articles = models.ManyToManyField(Article, blank=True)
    essays = models.ManyToManyField(Essay, blank=True)

    title = models.CharField(max_length=200, blank=True, default='')
    text = models.TextField(blank=True, default='')
    description = models.TextField(blank=True, default='')
    tag = models.ManyToManyField(Tag, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    comment = models.ManyToManyField(Comment, blank=True)


class RoadMapShareId(models.Model):
    roadmap = models.ForeignKey(RoadMap, on_delete=models.CASCADE)
    sha256 = models.CharField(max_length=64)

class EssayShareId(models.Model):
    essay = models.ForeignKey(Essay, on_delete=models.CASCADE)
    sha256 = models.CharField(max_length=64)


class Feedback(models.Model):
    text = models.TextField(default='')


class Term(models.Model):
    name = models.CharField(max_length=200, blank=True, default='')


class Newpaper(models.Model):
    term = models.ManyToManyField(Term, blank=True)
    text = models.TextField(blank=True, default='')

