from django.contrib.auth.models import Group
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    """
    group序列化类
    """
    # 加字段members
    def to_representation(self, instance):
        ret = super(GroupSerializer, self).to_representation(instance)
        ret["members"] = instance.user_set.count()
        return ret

    class Meta:
        model = Group
        fields = ("id", "name")


# 不支持添加/修改,只是把数据返回给前端
class UserGroupsSerializer(serializers.Serializer):
    """
    group序列化类
    """
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    class Meta:
        model = Group
        fields = ("id", "name")

