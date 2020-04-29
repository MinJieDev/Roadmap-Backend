from rest_framework import mixins, exceptions, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class UserRetrieveModelMixin(mixins.RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if instance.user != user:
            raise exceptions.PermissionDenied()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserListModelMixin(mixins.ListModelMixin):
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


class UserCreateModelMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserUpdateModelMixin(mixins.UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if instance.user != user:
            raise exceptions.PermissionDenied()

        data = request.data
        data['user'] = request.user.id

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class UserDestroyModelMixin(mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if instance.user != user:
            raise exceptions.PermissionDenied()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserModelViewSet(UserCreateModelMixin,
                       UserRetrieveModelMixin,
                       UserUpdateModelMixin,
                       UserDestroyModelMixin,
                       UserListModelMixin,
                       GenericViewSet):
    pass
