from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
# from rest_framework.throttling import
from app01 import models
from app01.utils.response_from import response_login

class myAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.GET.get('token')
        if token:
            user_token = models.User_token.objects.filter(token=token).first()
            if user_token:
                # 如果不return  user那么最后返回的是匿名用户
                return user_token.user,token
            else:
                raise AuthenticationFailed('fail')
        else:
            raise AuthenticationFailed('请求没有带token')


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        # 已经认证过了，request内部有user对象了，是当前的登录用户
        user = request.user
        # get_user_type_display()
        # get_字段名_display       这句话是因为user表中的choice字段的对应中文的显示
        # print(user.get_user_type_display())
        if user.user_type == 1:
            return True
        else:
            return False


# 自定义异常处理，统一错误的返回
# 日志记录（重要）
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):  # exc 是异常对象的信息，context是异常对象的具体信息
    response_data = response_login()
    # 一般来说会重新调用一下exception_handler函数，后面写自己的 处理逻辑
    response = exception_handler(exc, context)
    # 上面的函数执行完成有两种情况，一个是None，drf不处理，一个是response对象，但是处理不符合需求
    if not response:
        response_data.code = 1
        response_data.msg = str(exc)
        return Response(response_data.ResponseData())
    else:
        # return response
        response_data.code = 1
        response_data.msg = response.data.get('detail')
        return Response(data=response_data.ResponseData())


class myResponse(Response):
    def __init__(self, code=100 ,msg='请求成功', data=None, status=None, headers=None, **kwargs):
        dic = {
            'code':code,
            'msg':msg
        }
        if  data:
            dic = {
                'code': code,
                'msg': msg,
                'data': data
            }
        dic.update(kwargs)
        super().__init__(data=dic, status=status, headers=headers)


from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination


class myPagination(PageNumberPagination):
    page_size = 3   #每条页数
    page_query_param = 'page'   #查某一页的url中的key
    page_size_query_param = 'size'  # 每一页显示条数的key
    max_page_size = 5   # 每页最大显示条数