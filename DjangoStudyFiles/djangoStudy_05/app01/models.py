from django.db import models


class User(models.Model):
    name = models.CharField(max_length=32, verbose_name="姓名")
    password = models.CharField(max_length=32, verbose_name="密码")
    age = models.IntegerField(verbose_name="年龄")

