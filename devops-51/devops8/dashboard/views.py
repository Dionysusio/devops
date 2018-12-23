from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,QueryDict
from django.contrib.auth import authenticate,login
from django.views import View
from django.views.generic import View,TemplateView
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.contrib.auth.models import User,Group
from django.http import Http404
from django.core import serializers
from django.db import models


import json

def index(request):
    if request.method == "GET":
        print(request.GET)
        print(request.GET.getlist("aa"))
        print(request.GET.get("name"))
    elif request.method == "POST":
        print(request.POST)
    elif request.method == "DELETE":
        print(QueryDict(request.body))
    return HttpResponse("")



# def loginView(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#
#         user = authenticate(request,username=username,password=password)
#         if user is not None:
#             login(request,user)
#             return HttpResponse("用户登陆成功")
#         else:
#             return HttpResponse("用户登陆失败")
#     return render(request,'login.html')


def IndexView(request,*args,**kwargs):
    return HttpResponse("idnex view")



#函数视图
def login(request,*args,**kwargs):
    if request.method == "GET":
        return HttpResponse("展示用户界面")

    elif request.method == "POST":
        return HttpResponse("验证用户名与密码")

    return HttpResponse("")


#类视图
# class loginView(View):
#     def get(self,request,*args,**kwargs):
#         return HttpResponse("展示用户界面")
#
#     def post(self,request,*args,**kwargs):
#         return HttpResponse("验证用户名与密码")



class UserView(View):

    def get(self,request,*args,**kwargs):
        data = [{"id": user.id,"email":user.email} for user in User.objects.all()]
        return JsonResponse(data,safe=False)


class UserViewV2(View):
    def get(self,request,*args,**kwargs):
        queryset = User.objects.all()
        paginator = Paginator(queryset,10)
        try:
            page = int(request.GET.get("page"))
        except:
            page = 1
        if page<1:
            page = 1
        page = paginator.page(page)
        data = [{"id":user.id,"email":user.email,"username":user.email} for user in page.object_list]
        return JsonResponse(data,safe=False)


class UserViewV3(View):

    def post(self,request,*args,**kwargs):
        # 1.验证提交过来的参数
        # username = request.POST.get("username")
        # userpass = request.POST.get("userpass")
        # email = request.POST.get("email")
        data = request.POST.dict()

        try:
            user = User.objects.create_user(**data)
        except IntegrityError:
            return JsonResponse({"errmsg":"该用户已存在"})
        return JsonResponse({"id":user.id,"email":user.email,"username":user.username})



# class LoginView(View):
#     def get(self,request,*args,**kwargs):
#         return render(request,'login.html')
#
#     def post(self,request,*args,**kwargs):
#         return HttpResponse("验证用户名与密码")


class LoginVeiw(TemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        kwargs["title"] = "little amy"
        return kwargs



class GroupListView(View):
    def get(self,request,*args,**kwargs):
        queryset = Group.objects.all()
        return HttpResponse(serializers.serialize("json",queryset),content_type="application/json")


class GroupMembersView(View):

    def get_queryset(self):
        groupObj = self.get_group_obj()
        return groupObj.user_set.all()

    def get_group_obj(self):
        try:
            groupObj = Group.objects.get(name=self.request.GET.get("name"))
        except Group.DoesNotExist:
            raise Http404
        except Group.MultipleObjectsReturned:
            raise Http404
        return groupObj

    def get(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        return HttpResponse(serializers.serialize("json",queryset),content_type="application/json")


class UserGroupsView(View):

    def get_queryset(self):
        userObj = self.get_user_obj()
        return userObj.groups.all()

    def get_user_obj(self):
        try:
            userObj = User.objects.get(username=self.request.GET.get("username"))
        except User.DoesNotExist:
            raise Http404
        except User.MultipleObjectsReturned:
            raise Http404
        return userObj

    def get(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        return HttpResponse(serializers.serialize("json",queryset),content_type="application/json")




class UserGroupManageView(View):

    def get_group_obj(self):
        try:
            groupObj = Group.objects.get(name=QueryDict(self.request.body).get("groupname"))
        except Group.DoesNotExist:
            raise Http404
        return groupObj

    def get_user_obj(self):
        try:
            userObj = User.objects.get(username=QueryDict(self.request.body).get("username"))
        except User.DoesNotExist:
            raise Http404
        return userObj


    def delete(self,request,*args,**kwargs):
        """将用户从用户组中删除掉"""
        groupObj = self.get_group_obj()
        userObj = self.get_user_obj()
        groupObj.user_set.remove(userObj)
        return HttpResponse("")

    def put(self,request,*args,**kwargs):
        """将用户添加至指定用户组"""
        groupObj = self.get_group_obj()
        userObj = self.get_user_obj()
        groupObj.user_set.add(userObj)
        return HttpResponse("")


