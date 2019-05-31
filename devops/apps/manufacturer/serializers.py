#!/usr/bin/python3
#coding:utf-8

from rest_framework import serializers
from .models import Manufacturer
from .models import ProductModel


# 模型序列化类
class ManufacturerSerializer(serializers.ModelSerializer):
    # 和serializers.Serializer区别: 这个帮我们实现了create,update方法; 处理了字段
    class Meta:
        model = Manufacturer #指定模型
        fields = "__all__"   #要序列化的字段

    # 由于使用模型序列化类,所有数据都来源于模型,所以help_text 要在模型里加


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"

    # 如果使用模型序列化,不做处理,前端返回效果:
    # {
    #     "id":1,
    #     "model_name": "R710",
    #     "vendor":1
    # }
    # 这不是想要的效果,定义to_representation方法

    def validate_model_name(self, value):
        # validate_model_name  validate 下划线跟我们的字段名
        print(value)
        # print(value.lower()) 可以在这里进行二次加工数据. 上面是基础类型ManufacturerSerializer
        return value

    def validate(self, attrs):
        print(attrs)
        manufacturer_obj = attrs["vendor"]
        try:
            manufacturer_obj.productmodel_set.get(model_name__exact=attrs["model_name"])
            raise serializers.ValidationError("该型号已经存在")
        except ProductModel.DoesNotExist:
            return attrs

    def to_representation(self, instance):
        vendor = instance.vendor #获取所属制造商实例
        ret = super(ProductModelSerializer, self).to_representation(instance)
        ret["vendor"] = { #自定义返回字段
            "id": vendor.id,
            "name": vendor.vendor_name
        }
        return ret

    # to_representation处理之后前端返回效果:
    # {
    #     "id":1,
    #     "model_name":"R710",
    #     "vendor":{
    #         "id":1,
    #         "name":DELL
    #     }
    # }

