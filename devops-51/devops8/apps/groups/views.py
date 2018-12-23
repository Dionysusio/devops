# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, response, status
from .serializers import GroupSerializer, UserGroupsSerializer
from .filters import GroupFilter
from users.serializers import UserSerializer

User = get_user_model()

class GroupViewset(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_class = GroupFilter
    filter_fields = ("name",)


class UserGroupsViewset(viewsets.GenericViewSet,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin):

    queryset = User.objects.all()
    serializer_class = UserGroupsSerializer

    def retrieve(self, request, *args, **kwargs):
        userObj = self.get_object()
        queryset = userObj.groups.all()
        # 用户对应的所有组

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def update(self, request, *args, **kwargs):
        userObj = self.get_object()
        groupIds = request.data.get("gids", [])
        userObj.groups = Group.objects.filter(id__in=groupIds)
        return response.Response(status=status.HTTP_204_NO_CONTENT)



class GroupMembersViewset(viewsets.GenericViewSet,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin):

    serializer_class = UserSerializer
    queryset = Group.objects.all()

    def retrieve(self, request, *args, **kwargs):
        groupObj = self.get_object()
        queryset = groupObj.user_set.all()
        # 组下的所有用户

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # 删除组里的用户
        groupObj = self.get_object()
        userId = request.data.get("uid", 0)
        ret = {"status": 0}
        try:
            userObj = User.objects.get(pk=userId)
            groupObj.user_set.remove(userObj)
        except User.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "用户错误"
        return response.Response(ret, status=status.HTTP_200_OK)
