#!/usr/bin/python3
#coding:utf-8
from rest_framework import serializers
from .models import Idc


class IdcSerializer(serializers.Serializer):
    """Idc序列化"""
    id         = serializers.IntegerField(read_only=True)

    name       = serializers.CharField(required=True,max_length=32,label="机房名称",help_text="机房名称",
                                        error_messages={
                                           "blank":"机房名称不能为空",
                                           "required":"这个字段为必要字段"}
                                       )
    address    = serializers.CharField(required=True,max_length=200,label="机房地址",help_text="IDC详细地址",
                                       error_messages={
                                           "blank": "IDC详细地址不能为空",
                                           "required": "这个字段为必要字段"}
                                       )
    phone      = serializers.CharField(required=True,max_length=15,label="联系电话",help_text="联系电话",
                                       error_messages={
                                           "blank": "联系电话不能为空",
                                           "required": "这个字段为必要字段"}
                                       )
    email      = serializers.EmailField(required=True,label="email",help_text="email地址",
                                        error_messages={
                                            "blank": "email地址不能为空",
                                            "required": "这个字段为必要字段"}
                                        )
    letter     = serializers.CharField(required=True,max_length=5,label="字母简称",help_text="字母简称",
                                       error_messages={
                                           "blank": "字母简称不能为空",
                                           "required": "这个字段为必要字段"}
                                       )


    def create(self,validated_data):
       return Idc.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name       = validated_data.get("name",instance.name)
        instance.address    = validated_data.get("address",instance.address)
        instance.phone      = validated_data.get("phone",instance.phone)
        instance.email      = validated_data.get("email",instance.email)
        instance.save()
        return instance

    # 如果是readonly ,不需要定义上面2个方法,
    # 如果有更新,删除功能,create,update这2个方法必须定义,否则报错.



