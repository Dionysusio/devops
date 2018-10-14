from rest_framework import viewsets
# from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

User = get_user_model()

from .serializers import UserSerializer
from .filters import UserFilter


class UserViewset(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:返回指定用户信息
    list:返回用户列表
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # pagination_class = PageNumberPagination
    # pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = UserFilter
    filter_fields = ("username",) #搜索的字段


    # def get_queryset(self):
    #     queryset = super(UserViewset, self).get_queryset()
    #     username = self.request.query_params.get("username", None)
    #     if username:
    #         queryset = queryset.filter(username__icontains=username)
    #     return queryset









