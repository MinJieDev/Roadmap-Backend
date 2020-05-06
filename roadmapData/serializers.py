from rest_framework import serializers
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'email', 'username', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
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
        fields = ('id', 'title', 'description',
                  'user', 'articles', 'essays', 'road_maps')


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Feedback
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = '__all__'
