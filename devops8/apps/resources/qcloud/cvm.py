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
    credential = getCredential()
    return cvm_client.CvmClient(credential, region)

def getRegionCvmList(region):
    client = getCvmClient(region)
    req = models.DescribeInstancesRequest()
    resp = client.DescribeInstances(req)
    data = json.loads(resp.to_json_string())
    for instance in data["InstanceSet"]:
        saveInstance(instance)


def saveInstance(instance):
    data = {}
    data["cloud"] = "qcloud"
    data["instanceId"] = instance["InstanceId"]
    data["instanceType"] = instance["InstanceType"]
    data["cpu"] = instance["CPU"]
    data["memory"] = instance["Memory"]
    data["instanceName"] = instance["InstanceName"]
    data["createdTime"] = instance["CreatedTime"]
    data["expiredTime"] = instance["ExpiredTime"]
    #t_create = datetime.datetime.strptime(instance["CreatedTime"],"%Y-%m-%dT%H:%M:%SZ")
    data["hostname"] = "qcloud-cvm-{}".format(instance["InstanceId"])
    data["innerIps"] = instance["PrivateIpAddresses"]
    data["publicIps"] = instance["PublicIpAddresses"]
    print(data)

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

