from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from . import views

from .views import CreateOrGetRoadMapShareIdView, GetSharedRoadMapView, GetSharedEssayView, GetNewpaperView, CreateOrGetEssayShareIdView,RoadMapPutCommentView

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('articles', views.ArticleViewSet, basename='articles')
router.register('essays', views.EssayViewSet, basename='essays')
router.register('road_maps', views.RoadMapViewSet, basename='road_maps')
router.register('feedback', views.FeedbackViewSet, basename='feedback')
router.register('tags', views.TagViewSet, basename='tags')
router.register('terms', views.TermViewSet, basename='terms')
router.register('newpapers', views.NewpaperViewSet, basename='newpapers')
router.register('comments', views.CommentViewSet, basename='comments')

urlpatterns = [
    path('road_maps/<str:map_sha256>/', RoadMapPutCommentView.as_view()),
    path('', include(router.urls)),
    path('docs/', include_docs_urls(title='api', public=False)),
    path('login/', obtain_jwt_token),
    path('refresh/', refresh_jwt_token),
    path('verify/', verify_jwt_token),
    path('newpaper/<str:interest>/', GetNewpaperView.as_view()),
    path('share/roadmap/<str:map_sha256>/', GetSharedRoadMapView.as_view()),
    path('share/roadmap/', CreateOrGetRoadMapShareIdView.as_view()),
    path('share/essay/<str:map_sha256>/', GetSharedEssayView.as_view()),
    path('share/essay/', CreateOrGetEssayShareIdView.as_view()),
]
