
from django.http import HttpResponse
from .serializers import IdcSerializer,IDCSerializer
from .models import Idc
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser



class JSONResponse(HttpResponse):

    def __init__(self,data,**kwargs):
        kwargs.setdefault('content_type','application/json')
        content = JSONRenderer().render(data)
        super(JSONResponse, self).__init__(content=content,**kwargs)

# /idcs/
def idc_list(request, *args, **kwargs):
    if request.method == "GET":
        # 返回idc列表
        queryset = Idc.objects.all()
        serializer = IdcSerializer(queryset,many=True)
        return JSONResponse(serializer.data)
        # return HttpResponse(content,content_type="application\json")

    elif request.method == "POST":
        # 创建一个对象
        content = JSONParser().parse(request)
        serializer = IdcSerializer(data=content)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
            # return HttpResponse(content, content_type="application\json")


# /idcs/pk/
def idc_detail(request, pk, *args, **kwargs):
    try:
        idc = Idc.objects.get(pk=pk)
    except Idc.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = IdcSerializer(idc)
        return JSONResponse(serializer.data)

    elif request.method == "PUT":
        content = JSONParser().parse(request)
        serializer = IdcSerializer(idc, data=content)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)

    elif request.method == "DELETE":
        idc.delete()
        return HttpResponse(status=204)


########################### 版本二 ##############################################
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(["GET","POST"])
def idc_list_v2(request, *args, **kwargs):
    if request.method == "GET":
        # 返回idc列表
        queryset = Idc.objects.all()
        serializer = IdcSerializer(queryset,many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        # 创建一个对象
        content = JSONParser().parse(request)
        serializer = IdcSerializer(data=content)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET","PUT","DELETE"])
def idc_detail_v2(request, pk, *args, **kwargs):
    try:
        idc = Idc.objects.get(pk=pk)
    except Idc.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = IdcSerializer(idc)
        return Response(serializer.data)

    elif request.method == "PUT":
        content = JSONParser().parse(request)
        serializer = IdcSerializer(idc, data=content)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    elif request.method == "DELETE":
        idc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.reverse import reverse

@api_view(["GET"])
def api_root(request,format=None,*args,**kwargs):
    return Response({
        "idcs": reverse("idc-list",request=request,format=format)
    })



########################### 版本三 ##############################################
# 版本二和版本三功能一样,只不过一个是函数视图,一个是类视图

from rest_framework.views import APIView
from django.http import Http404

class IdcList(APIView):
    def get(self, request, format=None):  # 不需要位置参数了
        queryset = Idc.objects.all()
        serializer = IdcSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = IdcSerializer(data=request.data)
        # 如果使用了APIView,所有的数据都存放在request.data里
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class IdcDetail(APIView):
    def get_object(self, pk):
        try:
            return Idc.objects.get(pk=pk)
        except Idc.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        # 调用get_object,传一个pk
        idc = self.get_object(pk)
        serializer = IdcSerializer(idc)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        idc = self.get_object(pk)
        serializer = IdcSerializer(idc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        idc = self.get_object(pk)
        idc.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)



########################### 版本四 ##############################################
# 将具体的动作实现了,有queryset属性,跟数据库相关

from rest_framework import mixins,generics

class IdcList_V4(generics.GenericAPIView,  #框架类
                 mixins.ListModelMixin,    #实现get
                 mixins.CreateModelMixin): #实现post

    queryset = Idc.objects.all()
    serializer_class = IdcSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    #重写mixins.CreateModelMixin里的create方法
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


class IdcDetail_V4(generics.GenericAPIView,
                   mixins.RetrieveModelMixin, #实现get,获取指定一条记录
                   mixins.UpdateModelMixin,   #实现update
                   mixins.DestroyModelMixin): #实现delete

    queryset = Idc.objects.all()
    serializer_class = IdcSerializer

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)



##################################  版本五  ##############################################


class IdcList_V5(generics.ListCreateAPIView):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer

class IdcDetail_V5(generics.RetrieveUpdateDestroyAPIView):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer



##################################  版本六  ##############################################

# 处理复杂的url

from rest_framework import viewsets #导入viewsets,视图集

class IdcListViewset(viewsets.GenericViewSet,
    # ModelViewSet,其实可以只继承这个类,里面都帮我们实现好了所有方法
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):

    queryset = Idc.objects.all()
    serializer_class = IdcSerializer



##################################  版本七  ##############################################

from rest_framework import viewsets

class IdcListViewset_v7(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定用户信息

    list:
        返回用户列表

    update:
        更新IDC记录

    destroy:
        删除IDC记录

    create:
        创建IDC记录

    partial_update:
        更新部分字段
    """
    #继承viewsets.ModelViewSet这一个类,实现所有方法
    queryset = Idc.objects.all()
    serializer_class = IDCSerializer


