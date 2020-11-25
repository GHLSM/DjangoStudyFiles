from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=32)
    publish = models.CharField(max_length=64)
    author = models.CharField(max_length=32)


class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    user_type = models.IntegerField(choices=((1, '超级用户'), (2, '普通用户'), (3, '垃圾')))


class User_token(models.Model):
    token = models.CharField(max_length=64)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
