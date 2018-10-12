from rest_framework import viewsets
from .models import Manufacturer,ProductModel
from .serializers import ManufacturerSerializer,ProductModelSerializer


class ManufacturerViewset(viewsets.ModelViewSet):
    """
     retrieve:
         返回指定制造商信息

     list:
         返回制造商列表

     update:
         更新制造商记录

     destroy:
         删除制造商记录

     create:
         创建制造商记录

     partial_update:
         更新部分字段
     """
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class ProductModelViewset(viewsets.ModelViewSet):
    """
     retrieve:
         返回指定制造商信息

     list:
         返回制造商列表

     update:
         更新制造商记录

     destroy:
         删除制造商记录

     create:
         创建制造商记录

     partial_update:
         更新部分字段
     """
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer

