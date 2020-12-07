from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import Filter
import uuid
from rest_framework.request import Request
from app01 import models
from app01 import serializeFiles
from app01.utils.response_from import response_login
from app01.authenicateFiles import myAuth, UserPermission


class Books(ModelViewSet, APIView):
    authentication_classes = [myAuth]
    permission_classes = [UserPermission]
    queryset = models.Book.objects.all()
    serializer_class = serializeFiles.BookSer
    '''
    detail为布尔类型
    1.会自动生成一个路由
        <RegexURLPattern book-get-book-two ^books/get_book_two/$>
    2.action装饰器的methods的请求方式是指的当get请求从上面的路由来的时候来的时候会执行所装饰的函数
    3.detail表示生成带pk的路由
    '''
    @action(methods=['get'], detail=False)
    def get_book_two(self,request):
        print(request)
        book_obj = self.get_queryset()[:1]
        book_ser = self.get_serializer(book_obj, many=True)
        return Response(book_ser.data)


class Login(APIView):
    def post(self, request):
        Res = response_login()
        username = request.data.get('username')
        password = request.data.get('password')
        user_obj = models.User.objects.filter(username=username, password=password).first()
        if user_obj:
            Res.data = request.data
            Res.token = uuid.uuid4()
            # if not models.User_token.objects.filter(token=Res.token):
            #     models.User_token.objects.create(token=Res.token, user=user_obj)

            # update_or_create() 有就更新，没有就增加
            models.User_token.objects.update_or_create(defaults={'token':Res.token}, user=user_obj)
            return Response(Res.ResponseData())
        else:
            Res.code = 1
            Res.msg = 'fail'
            return Response(Res.ResponseData())


from rest_framework.generics import ListAPIView
class Books2(ListAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serializeFiles.BookSer
    filter_fields = ('id',)