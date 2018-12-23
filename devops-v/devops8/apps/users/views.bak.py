# -*- coding: utf-8 -*-


from rest_framework import viewsets,permissions
from .serializers import UserSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from django.contrib.auth import get_user_model
User = get_user_model()



class UserViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定user信息

    list:
        返回user列表

    update:
        更新user记录

    destroy:
        删除user记录

    create:
        创建user记录

    partial_update:
        更新部分字段
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # pagination_class = PageNumberPagination
    # permission_classes = (permissions.IsAuthenticated,)
    # 只要登陆就可以访问

