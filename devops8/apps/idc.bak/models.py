from django.db import models


class Idc(models.Model):
    name = models.CharField('IDC名称', max_length=100,blank=False,null=True)
    address = models.CharField('IDC地址', max_length=200,default='')
    phone = models.CharField('IDC联系电话', max_length=20,null=True)
    email = models.CharField('IDC邮箱', max_length=50)


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'idc'

