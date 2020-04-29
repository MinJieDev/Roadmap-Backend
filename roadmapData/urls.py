from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from . import views

from .views import CreateOrGetRoadMapShareIdView, GetSharedRoadMapView

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('articles', views.ArticleViewSet, basename='articles')
router.register('essays', views.EssayViewSet, basename='essays')
router.register('road_maps', views.RoadMapViewSet, basename='road_maps')
router.register('feedback', views.FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', include_docs_urls(title='api', public=False)),
    path('login/', obtain_jwt_token),
    path('refresh/', refresh_jwt_token),
    path('verify/', verify_jwt_token),
    path('share/roadmap/<str:map_sha256>/', GetSharedRoadMapView.as_view()),
    path('share/roadmap/', CreateOrGetRoadMapShareIdView.as_view())
]