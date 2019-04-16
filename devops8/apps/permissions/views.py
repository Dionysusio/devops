from rest_framework import viewsets, mixins, response, status
from django.contrib.auth.models import Permission, Group
from .serializers import PermissionSerializer


# 权限列表
class PermissionViewset(viewsets.GenericViewSet,
                        mixins.ListModelMixin):

    """
        list:
            获取权限列表
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


# 用户组权限
class GroupPermissionViewset(viewsets.GenericViewSet,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin):

    """
        retrieve:
            返回用户组的权限列表
        update:
            修改用户组的权限列表
    """
    queryset = Group.objects.all()
    serializer_class = PermissionSerializer

    def retrieve(self, request, *args, **kwargs):
        groupObj = self.get_object()
        queryset = groupObj.permissions.all()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def update(self, request, *args, **kwargs):
        ret = {"status":0}
        groupObj = self.get_object()

        pids = request.data.get("pids",[])
        #前端会拿到所有权限的id列表

        groupObj.permissions.set(Permission.objects.filter(pk__in=pids))
        #多对多关系使用groupObj.permission.set()方法指定,妈个鸡,和老师不一样的地方

        return response.Response(ret, status=status.HTTP_200_OK)

