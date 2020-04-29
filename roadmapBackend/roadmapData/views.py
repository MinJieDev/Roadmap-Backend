from rest_framework import viewsets, status, exceptions, mixins
from rest_framework import authentication
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from roadmapData import models
from roadmapData import serializers
from rest_framework.response import Response


class UserRetrieveModelMixin(RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if instance.user != user:
            return exceptions.PermissionDenied

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserListModelMixin(ListModelMixin):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user = request.user
        queryset = queryset.filter(user=user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserCreateModelMixin(CreateModelMixin):
    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserModelViewSet(UserCreateModelMixin,
                       UserRetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       UserListModelMixin,
                       GenericViewSet):
    pass


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


class ArticleViewSet(UserModelViewSet):
    queryset = models.Article.objects
    serializer_class = serializers.ArticleSerializer
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
