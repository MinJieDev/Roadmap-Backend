import json
import re
from _sha256 import sha256 as sha256_func

from django.http import HttpResponse, JsonResponse

from rest_framework import authentication, exceptions, mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import (CursorPagination, LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import (jwt_encode_handler,
                                            jwt_payload_handler)

from . import models, serializers
from .models import Article, RoadMap, RoadMapShareId
from .serializers import ArticleSerializer, RoadMapSerializer
from .utils import UserModelViewSet


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


class UserDefinePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class ArticleViewSet(UserModelViewSet):
    queryset = models.Article.objects
    serializer_class = serializers.ArticleSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = UserDefinePagination


class EssayViewSet(UserModelViewSet):
    queryset = models.Essay.objects
    serializer_class = serializers.EssaySerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = UserDefinePagination

class RoadMapViewSet(UserModelViewSet):
    queryset = models.RoadMap.objects
    serializer_class = serializers.RoadMapSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = UserDefinePagination

class GetSharedRoadMapView(APIView):
    ARTICLE_REG = re.compile(r'^\$(\d+)$')

    def get(self, request, map_sha256):
        roadmap = get_object_or_404(RoadMapShareId, sha256=map_sha256).roadmap
        serializer = RoadMapSerializer(roadmap)
        data = serializer.data
        roadmap_meta = json.loads(data['text'])
        nodes = roadmap_meta.get('nodes', [])
        picked_articles = []

        for node in nodes:
            title = node.get('text', '')
            pattern = self.ARTICLE_REG.match(title)
            if pattern is not None:
                article_id = int(pattern.group(1))
                picked_articles.append(article_id)
        picked_articles = Article.objects.filter(user=roadmap.user, id__in=picked_articles)
        picked_articles = ArticleSerializer(picked_articles, many=True).data
        data['articles'] = picked_articles
        return Response(data)


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


class TagViewSet(UserModelViewSet):
    queryset = models.Tag.objects
    serializer_class = serializers.TagSerializer
    permission_classes = (IsAuthenticated,)


class InterestsViewSet(UserModelViewSet):
    queryset = models.Interests.objects
    serializer_class = serializers.InterestsSerializer
