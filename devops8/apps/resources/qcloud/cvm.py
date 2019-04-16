#!/usr/bin/python
#coding:utf-8

import logging
import json
from resources.qcloud import getCredential
from tencentcloud.cvm.v20170312 import cvm_client, models
from resources.serializers import ServerSerializer

import datetime

logger = logging.getLogger(__name__)
REGIONS = ["ap-chongqing"]

def getCvmClient(region):
    credential = getCredential()  #获取证书
    return cvm_client.CvmClient(credential, region)


# 准备数据,将数据重新定义: 因为接口获取到的数据无法直接进行序列化
def getRegionCvmList(region):
    client = getCvmClient(regin)
    req = models.DescribeInstancesRequest()
    resp = client.DescribeInstances(req)
    data = json.loads(resp.to_json_string())
    print(data["InstanceSet"])  #返回多条记录
    for instance in data["InstanceSet"]:
        saveInstance(instance)  #调用saveInstance


def saveInstance(instance):
    data = {}  #准备一个空字典，存放最终的数据
    data["cloud"] = "qcloud"  #厂商,固定的
    data["instanceId"] = instance["InstanceId"]
    data["instanceType"] = instance["InstanceType"]
    data["cpu"] = instance["CPU"]
    data["memory"] = instance["Memory"]
    data["instanceName"] = instance["InstanceName"]
    data["createdTime"] = instance["CreatedTime"]
    data["expiredTime"] = instance["ExpiredTime"]
    data["hostname"] = "qcloud-cvm-{}".format(instance["InstanceId"]) # hostname字段服务器里没有，我们定义下，使用InstanceId
    data["innerIps"] = instance["PrivateIpAddresses"] #列表
    data["publicIps"] = instance["PublicIpAddresses"] #列表
    print(data)  # instance是从接口获取到的数据

    # 然后交给序列化,这是反序列化
    serializer = ServerSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        print("serializer.errors: ", serializer.errors)


def getCvmList():
    for region in REGIONS:
        try:
            getRegionCvmList(region)
        except Exception as e:
            print(e.args)

