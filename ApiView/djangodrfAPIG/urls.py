"""djangodrfAPIG URL Configuration

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
from rest_framework_jwt.views import ObtainJSONWebToken,RefreshJSONWebToken,VerifyJSONWebToken
# 上述三个类的基类是JSONWebTokenAPIView继承了APIView
'''
rest_framework_jwt.views内部源码有：
    obtain_jwt_token = ObtainJSONWebToken.as_view()
    refresh_jwt_token = RefreshJSONWebToken.as_view()
    verify_jwt_token = VerifyJSONWebToken.as_view()
'''
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^books/$', views.Books.as_view()),
    url(r'^books2/$', views.Books2.as_view()),
    url(r'^book/(?P<pk>\d+)', views.Book.as_view()),
    url(r'^book2/(?P<pk>\d+)', views.Book2.as_view()),

    url(r'^book6$', views.Books6.as_view(actions={
        'get': 'list','post': 'create'
    })),
    url(r'^book6/(?P<pk>\d+)', views.Books6.as_view(actions={
        'get': 'retrieve','put': 'update','delete': 'destroy'
    }))

]
