from app01 import models
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from app01.serializerFile import BookSer
from rest_framework.response import Response # drf提供的响应对象，二次封装
from rest_framework.renderers import JSONRenderer

class TestOne(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, pk):
        book = models.Book.objects.filter(pk=pk).first()
        # 实例化序列化器，要序列化谁，就传谁
        book_ser = BookSer(book)
        return Response(book_ser.data)

    # 修改数据
    def put(self, request, pk):
        # 初始化默认返回信息
        response_msg = {
            'status':1001,
            'msg':'success'
        }
        # 先找到这个对象
        book_obj = models.Book.objects.filter(pk=pk).first()
        # 得到序列化类的对象
        # book_ser = BookSer(book_obj, request.data) # request.data 是要修改的数据
        book_ser = BookSer(instance=book_obj, data=request.data) # request.data 是要修改的数据
        # 验证提交的数据是否符合要求，符合则保存，返回，不成功，返回错误信息
        if book_ser.is_valid():
            book_ser.save()  # 直接调save方法会直接报错
            # 添加返回数据信息
            response_msg["data"] = book_ser.data
            return Response(response_msg)
        else:
            response_msg['status'] = 1002
            response_msg['msg'] = 'fail'
            response_msg['data'] = book_ser.errors
            return Response(response_msg)
    def delete(self, request, pk):
        response_msg = {
            'status': 1001,
            'msg': 'success'
        }
        ret = models.Book.objects.filter(pk=pk).delete()
        return Response(response_msg)

class Books(APIView):
    def get(self, request):
        response_msg = {
            'status': 1001,
            'msg': 'success'
        }
        books = models.Book.objects.all()
        book_one = models.Book.objects.filter(pk=1)
        book_ser = BookSer(books, many=True) #many=True代表序列化多条数据，一个不需要写
        book_one_ser = BookSer(book_one)
        print(type(book_ser),type(book_one_ser))
        response_msg["data"] = book_ser.data
        return Response(response_msg)

    def post(self, request):
        response_msg = {
            'status': 1001,
            'msg': 'success'
        }
        # 修改时才有instance对象，新增不需要，只需要传入数据即可
        # book_ser = BookSer(request.data)  # 报错，因为第一个位置是instance
        book_ser = BookSer(data=request.data)
        if book_ser.is_valid():
            book_ser.save()
            response_msg["data"] = book_ser.data
        else:
            response_msg['status'] = 1002
            response_msg['msg'] = 'fail'
            response_msg['data'] = book_ser.errors
        return Response(response_msg)

