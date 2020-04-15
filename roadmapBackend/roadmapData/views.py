from rest_framework import viewsets, views
from django.contrib.auth.models import User
from roadmapData.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects
    serializer_class = UserSerializer
