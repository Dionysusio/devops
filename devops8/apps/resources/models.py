#!/usr/bin/python
#coding:utf-8


from django.db import models


class Cloud(models.Model):
    """ 云厂商"""
    name               = models.CharField("云厂商名称",max_length=50,help_text="云厂商名称")
    code               = models.CharField("云厂商名称",max_length=50,help_text="云厂商名称")

    def __str__(self):
        return self.code


# cloud 和server 是一对多关系
class Server(models.Model):
    """ 云服务器"""
    cloud              = models.ForeignKey(Cloud, on_delete=models.CASCADE,)
    instanceId         = models.CharField('实例ID', max_length=100,db_index=True,help_text='实例ID')
    instanceType       = models.CharField('实例类型',max_length=100,help_text='实例类型')
    cpu                = models.CharField('cpu', max_length=32,help_text='cpu')
    memory             = models.CharField('memory',max_length=32,help_text='memory')
    instanceName       = models.CharField('实例名称',max_length=100,db_index=True,help_text='实例名称')
    createdTime        = models.DateTimeField('创建时间',db_index=True)
    expiredTime        = models.DateTimeField('过期时间', db_index=True)
    hostname           = models.CharField('主机名',max_length=100,db_index=True)
    # server = Server.objects.get(pk=1)
    # server.innerIpAddress.all()
    # server.publicIpAddress.all()


class Ip(models.Model):
    """ server上的ip: ip,内网ip,外网ip"""
    ip                = models.GenericIPAddressField(db_index=True)
    inner             = models.ForeignKey(Server, related_name='innerIpAddress',null=True, on_delete=models.CASCADE,)
    public            = models.ForeignKey(Server,related_name='publicIpAddress',null=True, on_delete=models.CASCADE,)


