#!/usr/bin/python3
#coding:utf-8

from rest_framework import viewsets,mixins
from django.contrib.auth import get_user_model
from .serializers import GroupSerializer
from django.contrib.auth.models import Group

User = get_user_model()


class GroupUsersViewset(viewsets.GenericViewSet):

    # queryset = User.objects.all()
    serializer_class = GroupSerializer

    def get_group_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs,(
    		(self.__class__.__name__,lookup_url_kwarg)

    		)
        #pk
        filter_kwargs = {self.lookup_field:self.kwargs[lookup_url_kwarg]}
        return Group.objects.get(**filter_kwargs)

    def get_queryset(self):
        groupObj = self.get_group_object()
        return groupObj.user_set.all()

    def retrive(self,request,*args,**kwargs):
        #list的代码实现retrive方法
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset,many=True)
        return response.Response(serializer.data)

    def create(self,request,*args,**kwargs):
        groupObj = Group.objects.get(pk=request.data["gid"])
        userObj = User.objects.get(pk=request.data["uid"])
        groupObj.user_set.add(userObj)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self,request,*args,**kwargs):
        groupObj = self.get_group_object()
        userObj = User.objects.get(pk=request.data["uid"])
        groupObj.user_set.remove(userObj)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

