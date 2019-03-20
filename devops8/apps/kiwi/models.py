#!/usr/bin/python
#coding:utf-8

from django.db import models


# idc,az 一对多
class Idc(models.Model):
    """ Idc 机房"""
    name        =   models.CharField(max_length=30, verbose_name='所在机房', help_text='所在机房')
    tree_id     =   models.IntegerField(verbose_name='tree_id')
    # idc = Idc.objects.fiter()
    # idc = idc.idc_az.all()

    class Meta:
        verbose_name = 'IDC'
        ordering = ["id"]
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# az, fun 一对多
class AZ(models.Model):
    """AZ """
    name      =   models.CharField(max_length=20, verbose_name='AZ', help_text='AZ')
    idc       =   models.ForeignKey(Idc, related_name='idc_az', verbose_name="所在Idc", help_text="所在Idc", on_delete=models.CASCADE,)
    remark    =   models.CharField("备注", null=True,max_length=200, help_text="备注")
    # az = AZ.objects.fiter()
    # az.az_fun.all()

    class Meta:
        verbose_name = 'AZ管理'
        ordering = ["id"]
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# fun, subfun 一对多
class Function(models.Model):
    """ 功能大类"""

    name      =    models.CharField(max_length=30, verbose_name='功能大类', help_text='功能大类')
    name_en   =    models.CharField(max_length=30, null=True,verbose_name='功能大类英文', help_text='功能大类英文')
    az        =    models.ForeignKey(AZ, related_name='az_fun', verbose_name='所在AZ', help_text='所在AZ', on_delete=models.CASCADE,)
    # function = Function.objects.fiter()
    # function.fun_sub.all()

    class Meta:
        verbose_name = '功能大类'
        ordering = ["id"]
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Subfunction(models.Model):
    """ 功能小类"""

    name      =   models.CharField(max_length=30, verbose_name='功能小类', help_text='功能小类')
    name_en   =   models.CharField(max_length=30, null=True,verbose_name='功能小类英文', help_text='功能小类英文')
    function  =   models.ForeignKey(Function, related_name='fun_sub', verbose_name='所在功能大类', help_text='所在功能大类', on_delete=models.CASCADE,)

    class Meta:
        verbose_name = '功能小类'
        ordering = ["id"]
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


