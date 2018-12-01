from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Idc
from .serializers import IdcSerializer

# 将jsonresponse 单独抽出来
class JSONResponse(HttpResponse):
    def __init__(self,data,**kwargs):
        kwargs.setdefault('content_type','application/json')
        content = JSONRenderer().render(data)
        super(JSONResponse, self).__init__(content=content,**kwargs)


def idc_list(request,*args,**kwargs):
    if request.method == "GET":
        queryset = Idc.objects.all()
        serializer = IdcSerializer(queryset,many=True)
        return JSONResponse(serializer.data)
        # content = JSONRenderer().render(serializer.data)
        # return HttpResponse(content,content_type="application/json")
    elif request.method == "POST":
        data = JSONParser().parse(request)
        # print(data)
        serializer = IdcSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # content = JSONRenderer().render(serializer.data)
            # return HttpResponse(content, content_type="application/json")
            return JSONResponse(serializer.data)

def idc_detail(request,pk,*args,**kwargs):
    try:
        idc = Idc.objects.get(pk=pk)
    except Idc.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = IdcSerializer(idc)
        return JSONResponse(serializer.data)
    elif request.method == "PUT":
        content = JSONParser().parse(request)
        serializer = IdcSerializer(idc,data=content)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors,status=400)
    elif request.method == "DELETE":
        idc.delete()
        return HttpResponse(status=204)


##################################  版本二  ##############################################

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


@api_view(["GET","POST"])
#帮我们做了一个页面进行展示,可以提交的表单
def idc_list_v2(request,format=None,*args,**kwargs):
    if request.method == "GET":
        queryset = Idc.objects.all()
        serializer = IdcSerializer(queryset,many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = IdcSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET","PUT","DELETE"])
def idc_detail_v2(request,pk,format=None,*args,**kwargs):
    try:
        idc = Idc.objects.get(pk=pk)
    except Idc.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) #使用rest的Response,不需要JSON解析了

    if request.method == "GET":
        serializer = IdcSerializer(idc) #直接序列化,然后返回Response,省了很多代码
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = IdcSerializer(idc,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    elif request.method == "DELETE":
        idc.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


from rest_framework.reverse import reverse
@api_view(["GET"])
def  api_root(request,format=None,*args,**kwargs):
    return Response({
        # "idcs": "http://192.168.188.98:8000/idcs/"
        "idcs": reverse("idc-list",request=request,format=format),

    })


##################################  版本三  ##############################################

from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404

class IdcList(APIView):
#和上面的api_view效果是一样的;一个是函数视图,一个是类视图
    def get(self,request,format=None):
        queryset = Idc.objects.all()
        serializer = IdcSerializer(queryset,many=True)
        return Response(serializer.data)
    def post(self,request,format=None):
        serializer = IdcSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)


class IdcDetail(APIView):
    def get_object(self,pk): #将获取idc单独抽出来
        try:
            return Idc.objects.get(pk=pk)
        except Idc.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):
        idc = self.get_object(pk)
        serializer = IdcSerializer(idc)
        return Response(serializer.data)

    def put(self,request,pk,format=None):
        idc = self.get_object(pk)
        serializer = IdcSerializer(idc,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,pk,format=None):
        idc = self.get_object(pk)
        idc.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


##################################  版本四  ##############################################

from rest_framework import mixins,generics
#帮我们将具体的动作做出来了,
class IdcList_v4(generics.GenericAPIView,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    queryset = Idc.objects.all()
    #queryset跟数据库有关,从数据库查询记录.具体支持哪些,看源码GenericAPIView
    serializer_class = IdcSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class IdcDetail_v4(generics.GenericAPIView,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):

    queryset = Idc.objects.all()
    serializer_class = IdcSerializer

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)


##################################  版本五  ##############################################

class IdcList_v5(generics.ListCreateAPIView):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer

class IdcDetail_v5(generics.RetrieveUpdateDestroyAPIView):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer


##################################  版本六  ##############################################

from rest_framework import viewsets

class IdcListViewset(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.CreateModelMixin):

    queryset = Idc.objects.all()
    serializer_class = IdcSerializer


##################################  版本七  ##############################################

from rest_framework import viewsets

class IdcListViewset_v7(viewsets.ModelViewSet):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer

