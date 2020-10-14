from django.db import models


# Create your models here.
class User(models.Model):
    # id int primary_key auto_increment
    id = models.AutoField(primary_key=True)
    # username varchar(32)
    username = models.CharField(max_length=32)
    # password varchar(32)
    password = models.CharField(max_length=32)
