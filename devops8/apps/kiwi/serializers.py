#!/usr/bin/python
#coding:utf-8

from rest_framework import serializers
from .models import Idc, Function, Subfunction, AZ
from django.conf import settings


class SubfunctionSerializer(serializers.ModelSerializer):
    """
        功能小类序列化
    """

    class Meta:
        model = Subfunction
        fields = "__all__"

    def create(self,validated_data):
       return Subfunction.objects.create(**validated_data)


class FunctionSerializer(serializers.ModelSerializer):
    """ 功能大类序列化
        fun, subfun 一对多
    """
    fun_sub = SubfunctionSerializer(read_only=True,many=True)

    class Meta:
        model = Function
        fields = ('name', 'name_en', 'az', 'fun_sub')

    def create(self,validated_data):
       return Function.objects.create(**validated_data)



class AzSerializer(serializers.ModelSerializer):
    """ AZ序列化类
        az, fun 一对多
    """
    az_fun = FunctionSerializer(read_only=True,many=True)

    class Meta:
        model = AZ
        fields = ('name', 'idc', 'remark','az_fun')


    def create(self,validated_data):
       return AZ.objects.create(**validated_data)


    def to_representation(self,instance):
        result = super(AzSerializer, self).to_representation(instance)
        result['idc'] = {
            'id': instance.idc.id,
            'name': instance.idc.name
        }
        return result


class IdcSerializer(serializers.ModelSerializer):
    """ IDC序列化类
        idc, az 一对多
    """
    idc_az =AzSerializer(read_only=True, many=True)

    class Meta:
        model = Idc
        fields = ('name','tree_id','idc_az')

    def create(self,validated_data):
       return Idc.objects.create(**validated_data)

