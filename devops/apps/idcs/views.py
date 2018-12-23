from rest_framework import viewsets
from .models import Idc
from .serializers import IdcSerializer


class IdcListViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定用户信息

    list:
        返回用户列表

    update:
        更新IDC记录

    destroy:
        删除IDC记录

    create:
        创建IDC记录

    partial_update:
        更新部分字段
    """
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer

