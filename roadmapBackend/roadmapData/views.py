from rest_framework import viewsets, views
from django.contrib.auth.models import User
from roadmapData import models
from roadmapData import serializers
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects
    serializer_class = serializers.UserSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects
    serializer_class = serializers.ArticleSerializer


class ReadRecordViewSet(viewsets.ModelViewSet):
    queryset = models.ReadRecord.objects
    serializer_class = serializers.ReadRecordSerializer


class EssayViewSet(viewsets.ModelViewSet):
    queryset = models.Essay.objects
    serializer_class = serializers.EssaySerializer


class RoadMapViewSet(viewsets.ModelViewSet):
    queryset = models.RoadMap.objects
    serializer_class = serializers.RoadMapSerializer

    def list(self, request, *args, **kwargs):
        serializer = serializers.RoadMapViewSetSerializer(self.queryset, many=True)
        return Response(serializer.data)
