"""Django2vue URL Configuration

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
from jango_vue import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register', views.register, name='reg'),
    url(r'^login/', views.login, name='login'),
    # url(r'^get_code/', views.get_code, name='gc'),
    # url(r'^home/', views.home, name='home'),
    # url(r'^set_password/', views.set_password, name='set_pwd'),
    # url(r'^logout/', views.logout, name="logout"),
    #
    # # 暴露后端指定文件夹资源
    # url(r'^media/(?P<path>.*)',serve, {'document_root': settings.MEDIA_ROOT}),
    #
    # url(r'^up_and_down/', views.up_and_down),
    #
    # url(r'^comment/', views.comment),
    #
    # url(r'^(?P<username>\w+)/$', views.site, name='site'),
    #
    #
    # url(r'^(?P<username>\w+)/(?P<condition>category|tag|archive)/(?P<param>.*)', views.site),
    #
    # url(r'^(?P<username>\w+)/article/(?P<article_id>\d+)', views.article_detail),

]
