
from django.http import HttpResponse
from .serializers import IdcSerializer,IDCSerializer
from .models import Idc
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser



########################### 版本一 ##############################################

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
        # 直接从数据库拿的queryset是不干净的,序列化类可以帮我们拿到干净的数据,处理完是放在serializer.data里
        serializer = IdcSerializer(queryset,many=True)
        # 序列化,是将模型里的数据返回给前端!!!!!
        # 第一个参数:查询集queryset或者是模型的obj,第二个参数:如果是多条记录,many=True,如果是模型obj,many=False
        return JSONResponse(serializer.data)
        # 返回给前端

    elif request.method == "POST":
        # 序列化里有个动作: 保存数据到数据库
        content = JSONParser().parse(request)
        # 将提交过来的body里的数据进行转码,返回json格式的数据

        serializer = IdcSerializer(data=content)
        # 反序列化是将前端http post提交过来的json格式的数据 保存到数据库,需要提供data,是json格式的字符串!!!!!
        # 对json格式的数据进行序列化

        if serializer.is_valid():
            # 验证
            serializer.save()
            # 保存到数据库
            return JSONResponse(serializer.data)
            # 返回给前端
            # return HttpResponse(content, content_type="application\json")


# /idcs/pk/
def idc_detail(request, pk, *args, **kwargs):
    try:
        # 需要事先传入一个pk,获取要操作的对象,pk是表的唯一索引,不会存在多条记录,只会不存在,只要捕获不存在的异常
        idc = Idc.objects.get(pk=pk)
    except Idc.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        # 获取当个对象,交给序列化类
        serializer = IdcSerializer(idc)
        return JSONResponse(serializer.data)

    elif request.method == "PUT":
        # 更新一个对象,交给序列化类
        content = JSONParser().parse(request)
        serializer = IdcSerializer(idc, data=content)
        # 验证
        if serializer.is_valid():
            # 保存
            serializer.save()
            return JSONResponse(serializer.data)

    elif request.method == "DELETE":
        idc.delete()
        return HttpResponse(status=204)


########################### 版本二 ##############################################
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# 在函数的基础上封装了一层api_view,定义了方法就允许请求,否则不允许
@api_view(["GET","POST"])
def idc_list_v2(request, *args, **kwargs):
    if request.method == "GET":
        queryset = Idc.objects.all()
        serializer = IdcSerializer(queryset,many=True)
        return Response(serializer.data)

    elif request.method == "POST":
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
# 在APIView的基础上 将具体的动作实现了: 创建,修改,删除
# 查看GenericAPIView源码, 是在APIView的基础上做的一些事情
# 有queryset属性,只要有这个属性 就是跟数据库相关,从数据库拿东西,如果一个视图跟数据库没关系,就不用GenericAPIView

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
# generics.ListCreateAPIView,
# generics.RetrieveUpdateDestroyAPIView

class IdcList_V5(generics.ListCreateAPIView):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer

class IdcDetail_V5(generics.RetrieveUpdateDestroyAPIView):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer



##################################  版本六  ##############################################
# viewsets.GenericViewSet
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

#继承viewsets.ModelViewSet这一个类,实现所有方法
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

    queryset = Idc.objects.all()
    serializer_class = IDCSerializer


