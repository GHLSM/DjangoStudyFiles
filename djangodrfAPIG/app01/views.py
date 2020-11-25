from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from app01 import serializersFile
from app01 import models
from rest_framework.response import Response


class Books(APIView):
    def get(self, request):
        book_obj = models.Book.objects.all()
        books_ser = serializersFile.BooksSer(book_obj, many=True)
        return Response(books_ser.data)

    def post(self, request):
        book_ser = serializersFile.BooksSer(data=request.data)
        if book_ser.is_valid():
            book_ser.save()
            return Response(book_ser.data)


class Book(APIView):
    def get(self, request, pk):
        book_obj = models.Book.objects.filter(pk=pk).first()
        books_ser = serializersFile.BooksSer(book_obj)
        return Response(books_ser.data)

    def put(self, request, pk):
        book_obj = models.Book.objects.filter(pk=pk).first()
        book_ser = serializersFile.BooksSer(instance=book_obj, data=request.data)
        if book_ser.is_valid():
            book_ser.save()
            return Response(book_ser.data)

    def delete(self, request, pk):
        instance = models.Book.objects.filter(pk=pk).delete()
        return Response(instance)


class Books2(GenericAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serializersFile.BooksSer

    def get(self, request):
        book_obj = self.get_queryset()
        books_ser = self.get_serializer(book_obj, many=True)
        return Response(books_ser.data)

    def post(self, request):
        book_ser = self.get_serializer(data=request.data)
        if book_ser.is_valid():
            book_ser.save()
            return Response(book_ser.data)


class Book2(GenericAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serializersFile.BooksSer

    def get(self, request, pk):
        book_obj = self.get_object()
        books_ser = self.get_serializer(book_obj)
        return Response(books_ser.data)

    def put(self, request, pk):
        book_obj = self.get_object()
        book_ser = self.get_serializer(book_obj, request.data)
        if book_ser.is_valid():
            book_ser.save()
            return Response(book_ser.data)

    def delete(self, request, pk):
        instance = self.get_object().delete()
        return Response(instance)


from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin, ListModelMixin, RetrieveModelMixin


class Books3(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = models.Book.objects.all()
    serializer_class = serializersFile.BooksSer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class Book3(GenericAPIView, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin):
    queryset = models.Book.objects.all()
    serializer_class = serializersFile.BooksSer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)


from rest_framework.generics import ListAPIView, CreateAPIView, \
    DestroyAPIView, RetrieveAPIView, UpdateAPIView


class Books4(ListAPIView, CreateAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serializersFile.BooksSer


class Book4(DestroyAPIView, RetrieveAPIView, UpdateAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serializersFile.BooksSer


from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class Books5(ListCreateAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serializersFile.BooksSer


class Book5(RetrieveUpdateDestroyAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serializersFile.BooksSer


from rest_framework.viewsets import ModelViewSet


class Books6(ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializersFile.BooksSer


from rest_framework.viewsets import ViewSetMixin


class Books7(ViewSetMixin, APIView):
    # ViewSetMixin一定要放在最左边，查询父类时，第一个查询到ViewSetMixin内部重写的as_view方法
    def get_all_books(self, request):
        book_obj = models.Book.objects.all()
        books_ser = serializersFile.BooksSer(book_obj, many=True)
        return Response(books_ser.data)
