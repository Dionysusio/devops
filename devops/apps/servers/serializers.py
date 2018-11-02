#!/usr/bin/python3
#coding:utf-8

from rest_framework import serializers
from .models import Server,NetworkDevice,IP
from manufacturer.models import Manufacturer,ProductModel

class ServerAutoReportSerializer(serializers.Serializer):
    """
    服务器同步序列化类.
    这个地方的验证属于程序级别的验证.model是数据库级别的验证,能让程序验证的,就不要进数据库验证.
    """
    ip            =    serializers.IPAddressField(required=True)
    hostname      =    serializers.CharField(required=True,max_length=20)
    cpu           =    serializers.CharField(required=True,max_length=50)
    mem           =    serializers.CharField(required=True,max_length=20)
    disk          =    serializers.CharField(required=True,max_length=200)
    os            =    serializers.CharField(required=True,max_length=50)
    sn            =    serializers.CharField(required=True,max_length=50)
    # manufacturer  =    serializers.PrimaryKeyRelatedField(many=False,queryset=Manufacturer.objects.all())
    manufacturer  =    serializers.CharField(required=True)
    model_name    =    serializers.CharField(required=True)
    uuid          =    serializers.CharField(required=True,max_length=50)
    # network关联对象,接收的时候传一个json格式的数据,然后再处理
    network       =    serializers.JSONField(required=True)

    # 验证1,验证制造商字段manufacturer
    def validate_manufacturer(self, value):
        try: #检查vendor_name是否存在
            return Manufacturer.objects.get(vendor_name__exact=value)
        except Manufacturer.DoesNotExist:
            # 没有就创建,定义个创建的方法create_manufacturer,返回一个制造商的实例
            return self.create_manufacturer(value)

    # 验证2,对象级别验证,验证的是ServerAutoReportSerializer所有的数据
    def validate(self, attrs):
        # network = attrs["network"]
        # del attrs["network"] #取到,然后删掉. 因为数据库里没有这个字段,后面验证会报错
        manufacturer_obj = attrs["manufacturer"]
        try:
            attrs["model_name"] = manufacturer_obj.productmodel_set.get(model_name__exact=attrs["model_name"])
        except ProductModel.DoesNotExist:
            # 不存在就创建模型
            attrs["model_name"] = self.create_product_model(manufacturer_obj,attrs["model_name"])
        return attrs

    def create_server(self,validated_data):
        print("create")
        network = validated_data.pop("network") # 先拿出network数据,因为服务器没有这个字段
        server_obj = Server.objects.create(**validated_data) # 创建一个server记录
        # server_obj.networkdevice_set = network_queryset # 一对多关联
        self.check_server_network_device(server_obj,network)
        return server_obj

    def create(self, validated_data):
        """入口"""
        uuid = validated_data["uuid"].lower()
        sn = validated_data["sn"].lower()
        try: #区分虚拟机还是物理机
            if sn == uuid or sn == "" or sn.startswith("vmware"):
                # 虚拟机
                server_obj = Server.objects.get(uuid__icontains=uuid)
            else:
                # 物理机
                server_obj = Server.objects.get(sn__icontains=sn)
        except Server.DoesNotExist: #如果服务器不存在,就create
            return self.create_server(validated_data)
        else:# 否则就update,定义update_server
            return self.update_server(server_obj,validated_data)

    def update_server(self,instance,validated_data):
        print("update")
        instance.hostname = validated_data.get("hostanme",instance.hostname)#设置个默认值instance.hostname
        instance.cpu = validated_data.get("cpu",instance.cpu)
        instance.ip = validated_data.get("ip",instance.ip)
        instance.mem = validated_data.get("mem",instance.mem)
        instance.disk = validated_data.get("disk",instance.disk)
        instance.os = validated_data.get("os",instance.os)
        instance.save()
        self.check_server_network_device(instance,validated_data["network"])#更新network
        return instance

    def check_server_network_device(self,server_obj,network):
        """ 检查此服务器有没有这些网卡设备,并做关联 """
        network_device_queryset = server_obj.networkdevice_set.all()#取到当前服务器的所有网卡,之前的
        current_network_device_queryset = []#定义现在的网卡列表

        for device in network:
            try: #检查有没有当前设备名的网卡
                network_device_obj = network_device_queryset.get(name__exact=device["name"])
            except NetworkDevice.DoesNotExist:
                # 不存在则创建网卡,定义create_network_device
                network_device_obj = self.create_network_device(server_obj,device)
            self.check_ip(network_device_obj,device["ips"])#检查ip,要知道ip是在哪个网卡上面
            current_network_device_queryset.append(network_device_obj)#将现在的存到列表里

        for network_device_obj in set(network_device_queryset) - set(current_network_device_queryset):
            network_device_obj.delete()
            # 如果网卡改名了,需要将之前网卡以及所关联的ip全删除掉. 删掉之前有的,当前没有的

    def check_ip(self,network_device_obj,ifnets):
        # 拿到当前网卡的所有ip,检查ip在不在网卡上.不存在就创建ip,定义create_ip
        ip_queryset = network_device_obj.ip_set.all() #如果跟新了一个ip,ip_queryset就是之前的ip列表
        current_ip_queryset = [] #定义当前的ip列表
        for ifnet in ifnets: #遍历所有的ip
            try:
                ip_obj = ip_queryset.get(ifnet["ip_addr"])
            except IP.DoesNotExist:
                ip_obj = self.create_ip(network_device_obj,ifnet)
            current_ip_queryset.append(ip_obj) #将当前的ip存到ip列表里
        for ip_obj in set(ip_queryset) - set(current_ip_queryset):
            ip_obj.delete()
            # 1.换了ip地址
            # 2.新增一个ip
            # 3.删除了一个ip
                # 之前的ip列表,当前的ip列表,删掉之前有的,当前没有的:set(ip_queryset) - set(current_ip_queryset)
                # 网卡也一样

    def create_ip(self,network_device_obj,ifnet):
        ifnet["device"] = network_device_obj #需要指定ip所在的网卡设备
        return IP.objects.create(**ifnet)

    # 创建网卡,然后检查ip,定义check_ip
    def create_network_device(self,server_obj,device):
        ips = device.pop("ips")#拿到多个ip
        device["host"] = server_obj #网卡所在的主机,需要指定server_obj 实例
        network_device_obj = NetworkDevice.objects.create(**device)
        # self.check_ip(network_device_obj,ips)#检查ip,要知道ip是在哪个网卡上面
        return network_device_obj

    # 创建制造商对象
    def create_manufacturer(self,vendor_name):
        return Manufacturer.objects.create(vendor_name=vendor_name)
        #只要传vendor_name即可,其他字段可以为空

    # 创建模型对象
    def create_product_model(self,manufacturer_obj,model_name):
        return ProductModel.objects.create(model_name=model_name,vendor=manufacturer_obj)
        #传model_name,vendor(manufacturer_obj)字段

    def to_representation(self, instance):
        ret = {
            "hostname":instance.hostname,
            "ip":instance.ip
        }
        return ret

class ServerSerializer(serializers.ModelSerializer):
# class ServerSerializer(serializers.HyperlinkedModelSerializer):
    """服务器序列化类"""
    class Meta:
        model = Server
        fields = "__all__"

class NetworkDeviceSerializer(serializers.ModelSerializer):
    """
    网卡序列化
    """
    class Meta:
        model = NetworkDevice
        fields = "__all__"

class IPSerializer(serializers.ModelSerializer):
    """
    IP序列化
    """
    class Meta:
        model = IP
        fields = "__all__"

