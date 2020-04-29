from rest_framework import viewsets, status, mixins
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from roadmapData import models
from roadmapData import serializers
from rest_framework.response import Response

from roadmapData.utils import UserModelViewSet


class UserViewSet(mixins.CreateModelMixin,  # only CREATE is permitted
                  GenericViewSet):
    queryset = models.User.objects
    serializer_class = serializers.UserSerializer

    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['username'] = user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class ArticleViewSet(UserModelViewSet):
    queryset = models.Article.objects
    serializer_class = serializers.ArticleSerializer
    permission_classes = (IsAuthenticated,)


class EssayViewSet(UserModelViewSet):
    queryset = models.Essay.objects
    serializer_class = serializers.EssaySerializer
    permission_classes = (IsAuthenticated,)


class RoadMapViewSet(UserModelViewSet):
    queryset = models.RoadMap.objects
    serializer_class = serializers.RoadMapSerializer
    permission_classes = (IsAuthenticated,)


class FeedbackViewSet(mixins.CreateModelMixin,  # only CREATE is permitted
                      GenericViewSet):
    queryset = models.Feedback.objects
    serializer_class = serializers.FeedbackSerializer
