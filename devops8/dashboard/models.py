# coding:utf-8

from django.db import models



class Idc(models.Model):
    name = models.CharField(max_length=100,blank=False,null=True)
    address = models.CharField(max_length=200,default="")
    phone = models.CharField(max_length=20)
    user = models.CharField("IDC联系人",max_length=32,null=True)



class Manufacturer(models.Model):
    name = models.CharField(max_length=30)
    # car_set = Car.objects.filter(manufacturer=self.pk)


class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer,related_name="car_set")
    name = models.CharField(max_length=30)


