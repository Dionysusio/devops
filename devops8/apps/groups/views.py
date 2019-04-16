# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group
from rest_framework import viewsets, mixins, response, status
from .serializers import GroupSerializer, UserGroupsSerializer
from .filters import GroupFilter
from users.serializers import UserSerializer

from django.contrib.auth import get_user_model
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

    """
        retrieve:　
            获取当前用户所有的用户组
        update:
            修改当前用户的角色
    """

    # user模型
    # 因为操作的是用户,修改用户的用户组; queryset和序列化类不是一个model
    queryset = User.objects.all()

    # group序列化类
    # 为什么是这个序列化?序列化类中指定的model要和retrieve方法中queryset指定的model一致
    serializer_class = UserGroupsSerializer

    def retrieve(self, request, *args, **kwargs):
        # 获取指定用户对象,根据 queryset = User.objects.all()
        userObj = self.get_object()
        # 获取用户对应的所有组,然后交给序列化，做分页
        queryset = userObj.groups.all()

        # 复制 ListModelMixin 中的代码,支持搜索加分页:
        # 分页,有分页就做分页,否则直接序列化
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def update(self, request, *args, **kwargs):
        userObj = self.get_object()
        # 获取指定用户对象,drf自带的方法: self.get_object()
        # self.get_object() 会通过 User.objects.all() 去查询用户记录

        groupIds = request.data.get("gids", [])
        # 获取多个组,是id的形式

        # 多对多关系: user.group_set, 或者 user.groups
        # userObj.group_set = Group.objects.filter(id__in=groupIds) #给用户添加组
        userObj.groups.set(Group.objects.filter(id__in=groupIds))
        return response.Response(status=status.HTTP_204_NO_CONTENT)


# 角色成员管理
class GroupMembersViewset(viewsets.GenericViewSet,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin):
    """ retrieve:
            获取组下的成员列表
        destroy:
            从用户组里删除成员
    """

    queryset = Group.objects.all()

    # 返回的是组下的用户,所以使用用户序列化类
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # 组对象
        groupObj = self.get_object()
        # 组下的所有用户
        queryset = groupObj.user_set.all()
        page = self.paginate_queryset(queryset)  #分页
        if page is not None:
            serializer = self.get_serializer(page, many=True) #序列化
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        groupObj = self.get_object()
        userId = request.data.get("uid", 0)  #获取不到userobj,但是可以获取uid
        ret = {"status": 0}
        try:
            userObj = User.objects.get(pk=userId)
            groupObj.user_set.remove(userObj)
        except User.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "用户错误"
        return response.Response(ret, status=status.HTTP_200_OK)


