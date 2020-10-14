from django.shortcuts import render, HttpResponse, redirect
from app01 import models

# Create your views here.


def home(request):
    return render(request, "home.html")


def book_list(request):
    book_queryset = models.Book.objects.all()
    return render(request, 'book_list.html', locals())


def book_add(request):
    if request.method == 'POST':
        # 获取数据
        title = request.POST.get("title")
        price = request.POST.get("price")
        publish_date = request.POST.get("publish_date")
        publish_id = request.POST.get("publish")
        authors_list = request.POST.getlist("authors")
        # 存储数据
        book_obj = models.Book.objects.create(title=title,
                                              price=price,
                                              publish_date=publish_date,
                                              publish_id=publish_id)
        book_obj.authors.add(*authors_list)
        # 跳转页面
        return redirect('book_list')
    publish_queryset = models.Publish.objects.all()
    author_queryset = models.Author.objects.all()
    return render(request, 'book_add.html', locals())


def book_edit(request, edit_id):
    book_obj = models.Book.objects.filter(pk=edit_id).first()
    if request.method == 'POST':
        title = request.POST.get("title")
        price = request.POST.get("price")
        publish_date = request.POST.get("publish_date")
        publish_id = request.POST.get("publish")
        authors_list = request.POST.getlist("authors")
        models.Book.objects.filter(pk=edit_id).update(title=title,
                                                      price=price,
                                                      publish_date=publish_date,
                                                      publish_id=publish_id)
        book_obj.authors.set(authors_list)
        return redirect('book_list')
    publish_queryset = models.Publish.objects.all()
    author_queryset = models.Author.objects.all()

    return render(request, 'book_edit.html', locals())


def book_del(request, del_id):
    models.Book.objects.filter(pk=del_id).delete()
    return redirect('book_list')
