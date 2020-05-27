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
from .serializers import ArticleSerializer, RoadMapSerializer, RoadMapRecursiveSerializer, RoadMapSerializer, ArticleRecursiveSerializer, EssayRecursiveSerializer
from .utils import UserModelViewSet

from .models import Article, RoadMap, RoadMapShareId, User, Newpaper
from .serializers import ArticleSerializer, RoadMapSerializer
from .utils import UserModelViewSet, UserListModelMixin


class UserViewSet(mixins.CreateModelMixin,  # only CREATE is permitted
                  GenericViewSet,
                  mixins.UpdateModelMixin):
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

    def list(self, request, *args, **kwargs):
        queryset = User.objects
        user = request.user
        queryset = queryset.filter(username=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if instance.username != user.username:
            raise exceptions.PermissionDenied()
        data = request.data
        data['user'] = request.user.id

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


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

    def paginate_queryset(self, queryset):
        if self.paginator and self.request.query_params.get(self.paginator.page_query_param, None) is None:
            return None
        return super().paginate_queryset(queryset)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user = request.user
        queryset = queryset.filter(user=user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ArticleRecursiveSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ArticleRecursiveSerializer(queryset, many=True)
        return Response(serializer.data)

class EssayViewSet(UserModelViewSet):
    queryset = models.Essay.objects
    serializer_class = serializers.EssaySerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = UserDefinePagination
    
    def paginate_queryset(self, queryset):
        if self.paginator and self.request.query_params.get(self.paginator.page_query_param, None) is None:
            return None
        return super().paginate_queryset(queryset)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user = request.user
        queryset = queryset.filter(user=user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = EssayRecursiveSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = EssayRecursiveSerializer(queryset, many=True)
        return Response(serializer.data)

class RoadMapViewSet(UserModelViewSet):
    queryset = models.RoadMap.objects
    serializer_class = serializers.RoadMapSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = UserDefinePagination

    def paginate_queryset(self, queryset):
        if self.paginator and self.request.query_params.get(self.paginator.page_query_param, None) is None:
            return None
        return super().paginate_queryset(queryset)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user = request.user
        queryset = queryset.filter(user=user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = RoadMapRecursiveSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = RoadMapRecursiveSerializer(queryset, many=True)
        return Response(serializer.data)

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

    def paginate_queryset(self, queryset):
        if self.paginator and self.request.query_params.get(self.paginator.page_query_param, None) is None:
            return None
        return super().paginate_queryset(queryset)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user = request.user
        queryset = queryset.filter(user=user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        for i in range(len(serializer.data)):
            article_query = queryset[i].article_set.all()
            article_list = [j.id for j in article_query]
            essay_query = queryset[i].essay_set.all()
            essay_list = [j.id for j in essay_query]
            road_map_query = queryset[i].roadmap_set.all()
            road_map_list = [j.id for j in road_map_query]
  
            serializer.data[i]['articles'] = article_list
            serializer.data[i]['essays'] = essay_list
            serializer.data[i]['road_maps'] = road_map_list
          
        return Response(serializer.data)

class TermViewSet(viewsets.ModelViewSet):
    queryset = models.Term.objects
    serializer_class = serializers.TermSerializer


class NewpaperViewSet(viewsets.ModelViewSet):
    queryset = models.Newpaper.objects
    serializer_class = serializers.NewpaperSerializer


class GetNewpaperView(APIView):
    def get(self, request, interest):
        term = models.Term.objects.get(name=interest)
        newpapers = Newpaper.objects.filter(term=term.id).all()
        data =[]
        for newpaper in newpapers:
            serializer = serializers.NewpaperSerializer(newpaper)
            data.append(serializer.data)
        return Response(data)
