from django.db import models

# Create your models here.
'''
先写普通字段，在写外键
'''
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    phone = models.BigIntegerField(verbose_name='手机号', null=True, blank=True)
    """
    null告诉数据库可以为空
    blank告诉Django可以为空"""
    avatar = models.FileField(upload_to='avatar/', default='avatar/default.png', verbose_name='用户头像')
    create_time = models.DateField(auto_now_add=True)

    blog = models.OneToOneField(to='Blog', null=True)

    def __str__(self):
        return self.username


class Blog(models.Model):
    site_name = models.CharField(verbose_name='站点名称', max_length=32)
    site_title = models.CharField(verbose_name='站点标题', max_length=32)
    site_theme = models.CharField(verbose_name='站点样式', max_length=64)  # 存CSS或者JS的文件路径

    def __str__(self):
        return self.site_name


class Category(models.Model):
    name = models.CharField(verbose_name='文章分类', max_length=32)
    blog = models.ForeignKey(to='Blog', null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(verbose_name='文章标签', max_length=32)
    blog = models.ForeignKey(to='Blog', null=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(verbose_name='文章标题', max_length=64)
    desc = models.CharField(verbose_name='文章简介', max_length=255)
    '''文章内容较多，使用TextField'''
    content = models.TextField(verbose_name='文章内容')
    create_time = models.DateField(auto_now_add=True)
    '''点赞数'''
    up_num = models.BigIntegerField(default=0, verbose_name='点赞数')
    down_num = models.BigIntegerField(default=0, verbose_name='踩数')
    comment_num = models.BigIntegerField(default=0, verbose_name='评论数')
    # 外键字段
    blog = models.ForeignKey(to='Blog', null=True)
    category = models.ForeignKey(to='Category', null=True)
    tags = models.ManyToManyField(to='Tag', through='Article2Tag',
                                  through_fields=('article', 'tag'))

    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    article = models.ForeignKey(to='Article')
    tag = models.ForeignKey(to='Tag')


class UpAndDown(models.Model):
    user = models.ForeignKey(to='UserInfo')
    article = models.ForeignKey(to='Article')
    is_up = models.BooleanField()


class Comment(models.Model):
    user = models.ForeignKey(to='UserInfo')
    article = models.ForeignKey(to='Article')
    content = models.CharField(max_length=255)
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    # 自关联
    parent = models.ForeignKey(to='self', null=True)
