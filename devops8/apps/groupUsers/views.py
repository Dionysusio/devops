# -*- coding: utf-8 -*-

from rest_framework import viewsets, mixins, response, status
from django.http import QueryDict
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, GroupSerializer


User = get_user_model()

class GroupUserViewset(viewsets.GenericViewSet):

    serializer_class = UserSerializer

    def get_group_object(self):
        # 获取group对象
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        return Group.objects.get(**filter_kwargs)

    def get_queryset(self):
        # 获取指定组下的user列表
        groupObj = self.get_group_object()
        return groupObj.user_set.all()

    def retrieve(self, request, *args, **kwargs):
        # list的代码实现retrive方法
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset,many=True)
        return response.Response(serializer.data)


    def create(self,request,*args,**kwargs):
        # 往用户组里添加一个成员
        groupObj = Group.objects.get(pk=request.data['gid'])
        userObj = User.objects.get(pk=request.data['uid'])
        print('groupObj ==> {}'.format(groupObj))
        print('userObj ==> {}'.format(userObj))
        groupObj.user_set.add(userObj)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        # 从用户组中删除一个成员
        groupObj = self.get_group_object()
        userObj = User.objects.get(pk=request.data['uid'])
        print('groupObj ==> {}'.format(groupObj))
        print('userObj ==> {}'.format(userObj))
        groupObj.user_set.remove(userObj)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
