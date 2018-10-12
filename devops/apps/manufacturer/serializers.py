#!/usr/bin/python3
#coding:utf-8

from rest_framework import serializers
from .models import Manufacturer
from .models import ProductModel


class ManufacturerSerializer(serializers.ModelSerializer):
    # 由于使用模型序列化类,所有数据都来源于模型,所以help_text 要在模型里加
    class Meta:
        model = Manufacturer
        fields = "__all__"

class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"

    def validate_model_name(self,value):
        # validate_model_name  validate 下划线跟我们的字段名
        print(value)
        # print(value.lower()) 可以在这里进行二次加工数据. 上面是基础类型ManufacturerSerializer
        return value

    def validate(self, attrs):
        manufacturer_obj = attrs["vendor"]
        try:
            manufacturer_obj.productmodel_set.get(model_name__exact=attrs["model_name"])
            raise serializers.ValidationError("该型号已经存在")
        except ProductModel.DoesNotExist:
            return attrs

    def to_representation(self, instance):
        # ForeignKey 模型的序列化方法
        vendor = instance.vendor
        ret = super(ProductModelSerializer, self).to_representation(instance)
        ret["vendor"] = {
            "id": vendor.id,
            "name": vendor.vendor_name
        }
        return ret

