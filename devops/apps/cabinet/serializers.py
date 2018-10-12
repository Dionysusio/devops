#!/usr/bin/python3
#coding:utf-8
from  rest_framework import serializers
from idcs.serializers import IdcSerializer
from .models import Cabinet
from idcs.models import Idc

class CabinetSerializer(serializers.Serializer):
    # idc  =  serializers.IntegerField(required=True) #这只是个数字类型,不是我们想要的
    # idc  =  IdcSerializer(many=False) #many=True 对应多条记录,False对应单条记录.idc的所有字段都创建了,不是我们想要的
    idc  =  serializers.PrimaryKeyRelatedField(many=False,queryset=Idc.objects.all())
    # idc  =  serializers.SerializerMethodField() #只读,不需要关联关系,不能提交数据,不能反序列化,
    name =  serializers.CharField(required=True)

    # def get_idc(self,obj):
    #     """只读"""
    #     print(obj.idc)
    #     return {
    #         "id": obj.id,
    #         "name": obj.name
    #     }

    def to_representation(self, instance):
        # 自定义变更. 将上面的序列化字段转json. 是序列化转json前的最后一步
        # 靠关系的,需要代码实现的,可以在这里处理
        # print(instance)
        idc_obj = instance.idc
        ret = super(CabinetSerializer,self).to_representation(instance)
        ret["idc"] = {
            "id":idc_obj.id,
            "name": idc_obj.name
        }
        return ret

    def to_internal_value(self, data):
        """
        反序列化第一步:拿到的是提交过来的原始数据:QueryDict--> request.GET,request.POST
        然后进行验证,最终目的是把数据存到数据库,所以要验证
        是反序列化验证之前的第一步
        :param data:
        :return:
        """
        print(data) #反序列化,数据先到这里. 所有提交的数据.字段映射,验证
        return super(CabinetSerializer,self).to_internal_value(data)

    def create(self, validated_data):
        raise serializers.ValidationError("create error") #抛个异常
        return Cabinet.objects.create(**validated_data)














