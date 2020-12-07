from django.shortcuts import render, HttpResponse, redirect
from app01.myforms import MyRegForm
from app01 import models
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
import json
from django.db.models import F
from django.db import transaction


def register(request):
    back_dic = {'code': 1000, 'msg': ''}
    form_obj = MyRegForm()
    if request.method == "POST":
        # 校验数据
        form_obj = MyRegForm(request.POST)
        # 判断数据是否合法
        if form_obj.is_valid():
            clean_data = form_obj.cleaned_data
            clean_data.pop('confirm_pwd')
            file_obj = request.FILES.get(('avatar'))
            if file_obj:
                clean_data['avatar'] = file_obj
            models.UserInfo.objects.create_user(**clean_data)
            back_dic['url'] = '/login/'
        else:
            back_dic['code'] = 2000
            back_dic['msg'] = form_obj.errors
        return JsonResponse(back_dic)

    return render(request, 'register.html', locals())


def login(request):
    if request.method == 'POST':
        back_dic = {'code': 1000, 'msg': ''}
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        # 校验验证码
        if request.session.get('code').upper() == code.upper():
            # 校验用户名密码
            user_obj = auth.authenticate(request, username=username, password=password)
            if user_obj:
                # 保存用户状态
                auth.login(request, user_obj)
                back_dic['url'] = '/home/'
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '用户名或密码错误'
        else:
            back_dic['code'] = 3000
            back_dic['msg'] = '验证码错误'
        return JsonResponse(back_dic)
    return render(request, 'login.html')


'''
图片相关的模块 pillow
内存管理器模块  io
'''
from PIL import Image, ImageDraw, ImageFont  # 第一个为生成图片，第二个为在图片上画图，第三个为控制字体样式
from io import BytesIO, StringIO  # BytesIO临时存储数据，返回二进制数据 StringIO临时存储数据，返回字符串
import random


def get_random():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def get_code(request):
    # # 方式一
    # with open(r'static/img/01.png', 'rb') as f:
    #     data = f.read()
    # return HttpResponse(data)
    # # 方式二 利用pillow模块动态产生图片
    # img_obj = Image.new('RGB', (420, 35), get_random())
    # # 保存图片
    # with open('save_01', 'wb') as f:
    #     img_obj.save(f, 'png')
    # # 读取
    # with open('save_01', 'rb') as f:
    #     data = f.read()
    # return HttpResponse(data)
    # 方式三 内存管理器模块
    # img_obj = Image.new('RGB', (420, 35), get_random())
    # io_obj = BytesIO()  # 内存管理器对象，看成文件句柄
    # img_obj.save(io_obj, 'png')
    # return HttpResponse(io_obj.getvalue())  # 从内存管理器中读取二进制数据返回
    # 最终
    img_obj = Image.new('RGB', (420, 35), get_random())
    img_draw = ImageDraw.Draw(img_obj)  # 产生画笔对象
    img_font = ImageFont.truetype('static/font/hhh.ttf', 30)  # 字体样式

    code = ''
    for i in range(5):
        random_upper = chr(random.randint(65, 90))
        random_lower = chr(random.randint(97, 122))
        random_int = str(random.randint(0, 9))
        tmp = random.choice([random_int, random_lower, random_upper])  # 随机选一个
        """
        一个一个写以控制字间距
        """
        img_draw.text((i * 60 + 70, 0), tmp, get_random(), img_font)
        code += tmp

    # 存储验证码
    print(code)
    request.session['code'] = code
    io_obj = BytesIO()
    img_obj.save(io_obj, 'png')
    return HttpResponse(io_obj.getvalue())


def home(request):
    # 查询本网站所有的数据，展示到页面
    article_queryset = models.Article.objects.all()
    return render(request, 'home.html', locals())


@login_required
def set_password(request):
    if request.is_ajax():
        back_dic = {
            'code': 1000,
            'msg': '',
        }
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            is_right = request.user.check_password(old_password)
            if is_right:
                if new_password == confirm_password:
                    request.user.set_password(new_password)
                    request.user.save()
                    back_dic['msg'] = "修改成功"
                else:
                    back_dic['code'] = 2000
                    back_dic['msg'] = "两次密码不一致"
            else:
                back_dic['code'] = 3000
                back_dic['msg'] = "原密码错误"
            return JsonResponse(back_dic)


@login_required
def logout(request):
    auth.logout(request)
    return redirect(to="/home/")


def site(request, username, **kwargs):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    if not user_obj:
        return render(request, 'error.html')
    blog = user_obj.blog
    article_list = models.Article.objects.filter(blog=blog)

    if kwargs:
        condition = kwargs.get('condition')
        param = kwargs.get("param")
        if condition == "category":
            article_list = article_list.filter(category_id=param)
        elif condition == "tag":
            article_list = article_list.filter(tags__id=param)
        else:
            year, month = param.split('-')
            article_list = article_list.filter(create_time__year=year, create_time__month=month)

    category_list = models.Category.objects.filter(blog=blog).annotate(count_num=Count('article__pk')).values('name', 'count_num','pk')

    tag_list = models.Tag.objects.filter(blog=blog).annotate(count_num=Count('article__pk')).values('name', 'count_num','pk')

    time_list = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth('create_time')).values('month').annotate(count_num=Count('pk')).values('month', 'count_num')
    # print(time_list)
    return render(request, 'site.html', locals())


def article_detail(request, username, article_id):
    # 为了页面渲染
    user_obj = models.UserInfo.objects.filter(username=username).first()
    blog = user_obj.blog
    # 获取文章对象
    article_obj = models.Article.objects.filter(pk=article_id, blog__userinfo__username=username).first()
    if not article_obj:
        return render(request, 'error.html')
    comment_list = models.Comment.objects.filter(article=article_obj)
    return render(request, 'article_detail.html', locals())


def up_and_down(request):
    if request.is_ajax():
        back_dic = {
            'code': 1000,
            'msg': "",
        }
        if request.user.is_authenticated:
            article_id = request.POST.get('article_id')
            is_up = request.POST.get('is_up')
            # 转换
            is_up = json.loads(is_up)
            # 判断当前文章是否是用户自己写的
            article_obj = models.Article.objects.filter(pk=article_id).first()
            if not article_obj.blog.userinfo == request.user:
                is_click = models.UpAndDown.objects.filter(user=request.user, article=article_obj)
                if not is_click:
                    if is_up:
                        models.Article.objects.filter(pk=article_id).update(up_num=F('up_num') + 1)
                        back_dic['msg'] = "点赞成功"
                    else:
                        models.Article.objects.filter(pk=article_id).update(down_num=F('down_num') + 1)
                        back_dic['msg'] = "c踩成功"
                    models.UpAndDown.objects.create(user=request.user, article=article_obj, is_up=is_up)
                else:
                    back_dic['code'] = 2000
                    back_dic['msg'] = '您已经点过了哦'
            else:
                back_dic['code'] = 3000
                back_dic['msg'] = "自己不能给自己点哦"
        else:
            back_dic['code'] = 4000
            back_dic['msg'] = "请<a href='/login/'>登录</a>"

        return JsonResponse(back_dic)


def comment(request):
    if request.is_ajax():
        back_dic = {
            'code': 1000,
            'msg': ""
        }
        if request.method == 'POST':
            if request.user.is_authenticated:
                article_id = request.POST.get('article_id')
                parent_id = request.POST.get('parentId')
                content = request.POST.get('content')
                with transaction.atomic():
                    models.Article.objects.filter(pk=article_id).update(comment_num=F('comment_num') + 1)
                    models.Comment.objects.create(user=request.user, article_id=article_id, content=content,parent_id=parent_id)
                back_dic['msg'] = "评论成功"
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = "用户未登录"
            return JsonResponse(back_dic)















