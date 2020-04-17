from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    article_references = models.ManyToManyField("self", blank=True, null=True)

    title = models.CharField(max_length=200, blank=True, default='')
    author = models.CharField(max_length=200, blank=True, default='')
    journal = models.CharField(max_length=200, blank=True, default='')
    volume = models.IntegerField(blank=True, default=0)
    pages = models.IntegerField(blank=True, default=0)
    years = models.IntegerField(blank=True, default=0)
    url = models.URLField(max_length=200, default="")


class ReadRecord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    article = models.OneToOneField(Article, on_delete=models.CASCADE, blank=True, null=True)

    read_state = models.BooleanField(blank=True, default=False)
    text = models.TextField(blank=True, default='')


class Essay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    text = models.TextField(blank=True, default='')


class RoadMap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    articles = models.ManyToManyField(Article, blank=True, null=True)
    essays = models.ManyToManyField(Essay, blank=True, null=True)
    road_maps = models.ManyToManyField("self", blank=True, null=True)

    text = models.TextField(blank=True, default='')
