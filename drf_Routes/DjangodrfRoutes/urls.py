"""DjangodrfRoutes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views

# 1.导入模块
from rest_framework import routers
# 2.有两个类，实例化得到对象
#SimpleRouter
#DefaultRouter  生成的路由比较多
router = routers.SimpleRouter()
# router = routers.DefaultRouter()
# 3.注册
# router.register('前缀','继承自ModelViewSet的视图类','别名(用于方向解析)')
router.register(prefix='books',viewset=views.Books)  # 不用加斜杠了
# 3.5.看一眼路由的样子
# print(router.urls)
#[
#<RegexURLPattern book-list ^books/$>
#<RegexURLPattern book-detail ^books/(?P<pk>[^/.]+)/$>
# ]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^books/', views.Books.as_view(actions={'get': 'get_book_two'})),
    # url(r'^books/', views.Books.as_view(actions={'get': 'list', 'post': 'create'})),
    # url(r'^books/(?P<pk>\d+)', views.Books.as_view(actions={'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}))
    url(r'^login/', views.Login.as_view()),
    url(r'^books2/', views.Books2.as_view())
]
# 4.路由加进去，由于是列表，所以可以这样直接加
urlpatterns += router.urls

'''
router = routers.DefaultRouter()生成：

[
<RegexURLPattern book-list ^books/$>        和Simple一样
<RegexURLPattern book-list ^books\.(?P<format>[a-z0-9]+)/?$>    
    路由可以.json转换显示格式

<RegexURLPattern book-detail ^books/(?P<pk>[^/.]+)/$>       和Simple一样
<RegexURLPattern book-detail ^books/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$>
    路由可以/1.json转换显示格式
    
<RegexURLPattern api-root ^$>   根路径
<RegexURLPattern api-root ^\.(?P<format>[a-z0-9]+)/?$>
    路由可以.json转换显示格式
]
'''