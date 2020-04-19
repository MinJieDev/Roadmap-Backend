from django.urls import include, path
from roadmapData import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('articles', views.ArticleViewSet, basename='articles')
router.register('read_records', views.ReadRecordViewSet, basename='read_records')
router.register('essays', views.EssayViewSet, basename='essays')
router.register('road_maps', views.RoadMapViewSet, basename='road_maps')

urlpatterns = [
    path('api/', include(router.urls)),
]
