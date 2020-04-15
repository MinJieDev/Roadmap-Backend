from rest_framework import viewsets, views
from django.contrib.auth.models import User
from roadmapData.models import Article
from roadmapData.serializers import UserSerializer, ArticleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects
    serializer_class = UserSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects
    serializer_class = ArticleSerializer
