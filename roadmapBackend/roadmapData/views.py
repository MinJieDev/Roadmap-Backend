import json

from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status, mixins, exceptions
from rest_framework import authentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from roadmapData import models
from roadmapData import serializers
from rest_framework.response import Response

from roadmapData.utils import UserModelViewSet

from roadmapData.models import RoadMapShareId, RoadMap
from _sha256 import sha256 as sha256_func

from roadmapData.serializers import RoadMapSerializer


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


class GetSharedRoadMapView(APIView):
    def get(self, request, map_sha256):
        print(map_sha256)
        roadmap = get_object_or_404(RoadMapShareId, sha256=map_sha256).roadmap
        serializer = RoadMapSerializer(roadmap)
        print(serializer.data)
        return Response(serializer.data)


class CreateOrGetRoadMapShareIdView(APIView):
    def post(self, request):
        try:
            road_map_id = json.loads(request.body)['id']
        except:
            raise exceptions.ParseError()

        roadmap = get_object_or_404(RoadMap, id=road_map_id)

        if roadmap.user != request.user:
            self.permission_denied(request)

        code = 'roadmap{}'.format(road_map_id)
        sha256 = sha256_func(code.encode()).hexdigest()
        try:
            record = RoadMapShareId.objects.get(sha256=sha256)
            record.roadmap = roadmap
        except RoadMapShareId.DoesNotExist:
            record = RoadMapShareId.objects.create(sha256=sha256,
                                                   roadmap=roadmap)
        record.save()
        return Response({'share_id': sha256})


class FeedbackViewSet(mixins.CreateModelMixin,  # only CREATE is permitted
                      GenericViewSet):
    queryset = models.Feedback.objects
    serializer_class = serializers.FeedbackSerializer
