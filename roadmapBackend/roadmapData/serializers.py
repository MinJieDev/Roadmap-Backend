from rest_framework import serializers
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from roadmapData import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('username', 'email', 'password', 'token')

    def create(self, validated_data):
        user = super().create(validated_data)

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.set_password(validated_data['password'])
        user.save()

        user.token = token
        return user


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
        fields = ('id', 'title', 'description',
                  'user', 'articles', 'essays', 'road_maps')
