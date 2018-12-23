#!/usr/bin/python
#coding:utf-8

from django.conf  import settings
from tencentcloud.common import credential


def getCredential():
    return credential.Credential(settings.QCLOUD_SECRETID,settings.QCLOUD_SECRETKEY)