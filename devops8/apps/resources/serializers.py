#!/usr/bin/python
#coding:utf-8

import logging
from rest_framework import serializers
from .models import Server, Cloud, Ip
import datetime

logger = logging.getLogger(__name__)

class ServerSerializer(serializers.Serializer):
    id              = serializers.ReadOnlyField()
    cloud           = serializers.PrimaryKeyRelatedField(queryset=Cloud.objects.all(), many=False)
    instanceId      = serializers.CharField(required=True)
    instanceType    = serializers.CharField(required=True)
    cpu             = serializers.CharField(required=True)
    memory          = serializers.CharField(required=True)
    instanceName    = serializers.CharField(required=True)
    createdTime     = serializers.DateTimeField(required=True,format="%Y-%m-%d %H:%M:%S")
    expiredTime     = serializers.DateTimeField(required=True,format="%Y-%m-%d %H:%M:%S")
    hostname        = serializers.CharField(required=True)
    publicIps       = serializers.ListField(required=True,write_only=True)
    innerIps        = serializers.ListField(required=True,write_only=True)

    class Meta:
        model = Server
        fields = "__all__"

    # 将 cloud换成qcloud对应的id值
    def getCloudPk(self, code):
        try:
            obj = Cloud.objects.get(code__exact=code)
            return obj.id
        except Cloud.DoesNotExist: #参数是code,不是pk,不是唯一的,会报错
            logger.error("云厂商不存在: {}".format(code))
            raise serializers.ValidationError("云厂商不存在")
        except Exception as e:
            logger.error("云厂商错误: ".format(e.args))
            raise serializers.ValidationError("云厂商错误")

    # 改变cloud的值
    def to_internal_value(self, data):
        data["cloud"] = self.getCloudPk(data["cloud"]) #改变下cloud的值,调用getCloudPk
        print("to_internal_value: ", data)
        return super(ServerSerializer, self).to_internal_value(data)


    def getInstance(self, instanceId):
        try:
            return Server.objects.get(instanceId__exact=instanceId)
        except Server.DoesNotExist:
            return None
        except Exception as e:
            logger.error("服务器错误: ".format(e.args))
            raise serializers.ValidationError("服务器错误")

    def create(self, validated_data):
        instance = self.getInstance(validated_data["instanceId"])
        if instance is not None:
            return self.update(instance, validated_data)
        innerIps = validated_data.pop("innerIps")
        publicIps = validated_data.pop("publicIps")
        instance = Server.objects.create(**validated_data)
        self.check_inner_ip(instance, innerIps)
        self.check_public_ip(instance, publicIps)
        return instance

    def update(self, instance, validated_data):
        instance.cpu = validated_data.get("cpu", "")
        self.check_inner_ip(instance, validated_data['innerIps'])
        self.check_public_ip(instance, validated_data['publicIps'])
        instance.save()
        return instance

    def check_inner_ip(self, instance, innerIps):
        ip_queryset = instance.innerIpAddress.all()
        current_ip_objs = []
        for ip in innerIps:
            try:
                ip_obj = ip_queryset.get(ip__exact=ip)
            except Ip.DoesNotExist:
                ip_obj = Ip.objects.create(ip=ip, inner=instance)
            current_ip_objs.append(ip_obj)
        self.cleanip(ip_queryset, current_ip_objs)

    def check_public_ip(self, instance, publicIps):
        ip_queryset = instance.publicIpAddress.all()
        current_ip_objs = []
        for ip in publicIps:
            try:
                ip_obj = ip_queryset.get(ip__exact=ip)
            except Ip.DoesNotExist:
                ip_obj = Ip.objects.create(ip=ip, public=instance)
            current_ip_objs.append(ip_obj)
        self.cleanip(ip_queryset, current_ip_objs)


    def cleanip(self, ip_queryset, current_ip_objs):
        not_exists_ip = set(ip_queryset) - set(current_ip_objs)
        for obj in not_exists_ip:
            obj.delete()

    def to_representation(self,instance):
        ret = super(ServerSerializer, self).to_representation(instance)

        ret['cloud'] = {
            'id': instance.cloud.id,
            'name': instance.cloud.name
        }

        # result['publicIps'] = [ip.ip for ip in instance.publicIpAddress.all()]
        # result['innerIps'] = [ip.ip for ip in instance.innerIpAddress.all()]

        ret["publicIps"] = []
        ret["innerIps"] = []

        for ip in instance.publicIpAddress.all(): #遍历所有的外网ip
            print(ip.ip)
            ret["publicIps"].append(ip.ip)

        for ip in instance.innerIpAddress.all():
            ret["innerIps"].append(ip.ip)

        return ret

