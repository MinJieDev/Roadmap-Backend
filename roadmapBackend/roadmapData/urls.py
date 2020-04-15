from django.urls import include, path
from roadmapData import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('articles', views.ArticleViewSet, basename='articles')
router.register('essays', views.EssayViewSet, basename='essays')

urlpatterns = [
    path('', include(router.urls)),
]
