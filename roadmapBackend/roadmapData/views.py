from rest_framework import viewsets, views
from django.contrib.auth.models import User
from roadmapData import models
from roadmapData import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects
    serializer_class = serializers.UserSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects
    serializer_class = serializers.ArticleSerializer


class EssayViewSet(viewsets.ModelViewSet):
    queryset = models.Essay.objects
    serializer_class = serializers.EssaySerializer
