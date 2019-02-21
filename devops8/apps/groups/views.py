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


#这个视图的作用: 提交修改用户组,展示给前端
class UserGroupsViewset(viewsets.GenericViewSet,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin):

    # 这个queryset和序列化类可以不是一个model
    queryset = User.objects.all()

    # 序列化中指定的model要和retrieve方法中的queryset一致才行
    serializer_class = UserGroupsSerializer #为什么是这个序列化?

    def retrieve(self, request, *args, **kwargs):
        # 获取用户, self.get_object() 会通过 User.objects.all()去查询用户记录
        userObj = self.get_object()

        # 用户对应的所有组
        queryset = userObj.groups.all()

        #复制 ListModelMixin 中的代码,支持搜索加分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def update(self, request, *args, **kwargs):
        userObj = self.get_object() #获取指定用户记录,这是什么方法?
        # self.get_object() 会通过 User.objects.all()去查询用户记录

        groupIds = request.data.get("gids", []) #获取多个组,是id的形式

        # 多对多: user_group_set, 或者 user_groups = 列表
        userObj.groups = Group.objects.filter(id__in=groupIds) #给用户添加组

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
