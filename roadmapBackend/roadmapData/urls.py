from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from roadmapData import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('articles', views.ArticleViewSet, basename='articles')
router.register('read_records', views.ReadRecordViewSet, basename='read_records')
router.register('essays', views.EssayViewSet, basename='essays')
router.register('road_maps', views.RoadMapViewSet, basename='road_maps')
router.register('feedback', views.FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/docs/', include_docs_urls(title='api', public=False)),
    path('api/login/', obtain_jwt_token),
    path('api/refresh/', refresh_jwt_token),
    path('api/verify/', verify_jwt_token),
]
