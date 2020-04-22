from rest_framework import serializers
from django.contrib.auth.models import User
from roadmapData import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = '__all__'


class ReadRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReadRecord
        fields = '__all__'


class EssaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Essay
        fields = '__all__'


class RoadMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoadMap
        fields = '__all__'


class RoadMapViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoadMap
        fields = ('title', 'description',
                  'user', 'articles', 'essays', 'road_maps')
