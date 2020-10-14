from django.shortcuts import render, HttpResponse, redirect
from app01 import models


# Create your views here.
def index(request):
    """
    :param request:
    :return:
    """
    # return HttpResponse("你好啊")
    # 返回html,自动去文件夹下查找文件
    return render(request, 'first_01.html')
    # return redirect('https://www.mzitu.com')


def ab_render(request):
    user_dic = {'username': 'gh', 'age': 18}
    # 第一种方式
    # return render(request, 'first_01.html', {'data': user_dic})
    # 第二种方式
    return render(request, 'first_01.html', locals())


def login(request):
    # if request.method == 'GET':
    #     return render(request, 'login.html')
    # elif request.method == 'POST':
    #     return HttpResponse("收到")
    if request.method == 'POST':
        # 获取用户数据
        # print(request.POST)
        # <QueryDict: {'username': ['gh'], 'password': ['123']}>
        # get只会拿到列表最后一个元素
        # username = request.POST.get("username")
        # 使用getlist
        username = request.POST.get("username")
        password = request.POST.get('password')

        # res = models.User.objects.filter(username=username)
        # user_obj = res[0]
        # select * from User where username='jason';
        user_obj = models.User.objects.filter(username=username).first()
        # print(user_obj)
        if user_obj:
            # 比对密码是否一致
            if password == user_obj.password:
                return HttpResponse("登陆成功")
            else:
                return HttpResponse("密码错误")
        else:
            return HttpResponse("用户不存在")

        # return HttpResponse("收到")
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def userlist(request):
    # data = models.User.objects.filter()
    # print(data)
    user_query = models.User.objects.all()
    # print(user_query)
    return render(request, 'userlist.html', locals())

    # return HttpResponse("userlist")


def edit_user(request):
    # 获取url后面的参数
    edit_id = request.GET.get('user_id')
    # 查询当前用户像编辑的数据对象
    edit_obj = models.User.objects.filter(id=edit_id).first()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 修改数据方式一
        models.User.objects.filter(id=edit_id).update(username=username, password=password)

        # # 修改数据方式二,缺点：当字段特别多的时候效率会很低
        # edit_obj.username = username
        # edit_obj.password = password
        # edit_obj.save()

        # 跳转到数据展示界面
        return redirect('/userlist/')

    return render(request, 'edit_user.html', locals())


def del_user(request):
    del_id = request.GET.get('user_id')
    # 批量删除
    models.User.objects.filter(id=del_id).delete()
    return redirect('/userlist/')









