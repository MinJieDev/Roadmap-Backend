from rest_framework import viewsets, status
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from roadmapData import models
from roadmapData import serializers
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
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


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects
    serializer_class = serializers.ArticleSerializer
    permission_classes = (IsAuthenticated,)


class ReadRecordViewSet(viewsets.ModelViewSet):
    queryset = models.ReadRecord.objects
    serializer_class = serializers.ReadRecordSerializer
    permission_classes = (IsAuthenticated,)


class EssayViewSet(viewsets.ModelViewSet):
    queryset = models.Essay.objects
    serializer_class = serializers.EssaySerializer
    permission_classes = (IsAuthenticated,)


class RoadMapViewSet(viewsets.ModelViewSet):
    queryset = models.RoadMap.objects
    serializer_class = serializers.RoadMapSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        serializer = serializers.RoadMapViewSetSerializer(self.queryset, many=True)
        return Response(serializer.data)


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = models.Feedback.objects
    serializer_class = serializers.FeedbackSerializer
    permission_classes = (IsAuthenticated,)
