# -*- coding: utf-8 -*-

from rest_framework import viewsets, permissions, mixins
from .serializers import UserSerializer, UserRegSerializer
from rest_framework.pagination import PageNumberPagination
from .filters import UserFilter
from django.contrib.auth import get_user_model
User = get_user_model()


class UserViewset(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer
    filter_class = UserFilter
    filter_fields = ("username",)



class UserRegViewset(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin):

    queryset = User.objects.all()
    serializer_class = UserRegSerializer