#!/usr/bin/python3
#coding:utf-8

from rest_framework import serializers
from .models import Idc



class IDCSerializer(serializers.ModelSerializer):
    """模型序列化"""
    class Meta:
        model = Idc
        fields = "__all__"
        # fields = ('name', 'address', 'phone') 序列化部分字段


class IdcSerializer(serializers.Serializer):
    """Idc序列化"""
    id         = serializers.IntegerField(read_only=True)

    name       = serializers.CharField(required=False,help_text="机房名称",
                                        error_messages={
                                           "blank":"机房名称不能为空",
                                           "required":"这个字段为必要字段"})
    address    = serializers.CharField(required=False,help_text="IDC详细地址",
                                       error_messages={
                                           "blank": "IDC详细地址不能为空",
                                           "required": "这个字段为必要字段"})
    phone      = serializers.CharField(required=False,help_text="联系电话",
                                       error_messages={
                                           "blank": "联系电话不能为空",
                                           "required": "这个字段为必要字段"})
    email      = serializers.EmailField(required=False,help_text="email地址",
                                        error_messages={
                                            "blank": "email地址不能为空",
                                            "required": "这个字段为必要字段"})


    def create(self,validated_data):
       return Idc.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.name       = validated_data.get("name",instance.name)
        instance.address    = validated_data.get("address",instance.address)
        instance.phone      = validated_data.get("phone",instance.phone)
        instance.email      = validated_data.get("email",instance.email)
        instance.save()
        return instance


    def to_internal_value(self,data):
        #这是反序列化的第一步,post提交之后,先实例化IdcSerializer,然后再调每个字段的to_internal_value方法
        #然后调用update,create.
        #增加减少字段,修改字段的值可以通过这个方法实现.
        print(data)
        return super(IdcSerializer,self).to_internal_value(data)


    def to_representation(self,instance):
        #这个方法是序列化最后一步,自定义显示给前端的数据,想怎么定义就怎么定义,和模型字段没太大关系
        ret = super(IdcSerializer,self).to_representation(instance)
        return ret

