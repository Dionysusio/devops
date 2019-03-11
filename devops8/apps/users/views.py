# -*- coding: utf-8 -*-

from rest_framework import viewsets, permissions, mixins, response, status
from .serializers import UserSerializer, UserRegSerializer
from .filters import UserFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
User = get_user_model()


# 视图控制: 能提交哪些方法
# 这里不允许创建
class UserViewset(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    # queryset = User.objects.filter(is_superuser=False) #过滤掉超级用户
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter
    filter_fields = ("username",)


class UserRegViewset(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin):

    queryset = User.objects.all()
    serializer_class = UserRegSerializer


class UserInfoViewset(viewsets.ViewSet):
    """ JWT反解之后得到的用户数据"""

    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        data = {
            "username": self.request.user.username,
            "name": self.request.user.name,
            "permission": self.request.user.get_all_permissions()
        }
        return response.Response(data)

