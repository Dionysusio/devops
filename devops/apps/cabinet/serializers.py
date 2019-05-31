#!/usr/bin/python3
#coding:utf-8

from  rest_framework import serializers
from  .models import Cabinet
from  idcs.models import Idc


class CabinetSerializer(serializers.Serializer):
    idc  =  serializers.PrimaryKeyRelatedField(many=False,queryset=Idc.objects.all())
    # idc  =  serializers.SerializerMethodField() 只读
    name =  serializers.CharField(required=True)

    def to_representation(self, instance):
        idc_obj = instance.idc
        ret = super(CabinetSerializer,self).to_representation(instance)
        ret["idc"] = {
            "id": idc_obj.id,
            "name": idc_obj.name
        }
        return ret

    def to_internal_value(self, data):
        """
        反序列化第一步: 拿到的是提交过来的原始数据:QueryDict--> request.GET,request.POST
        然后进行验证,

        """
        print(data) #反序列化,数据先到这里. 所有提交的数据.字段映射,验证
        return super(CabinetSerializer,self).to_internal_value(data)

    def create(self, validated_data):
        # raise serializers.ValidationError("create error") #抛个异常
        return Cabinet.objects.create(**validated_data)


