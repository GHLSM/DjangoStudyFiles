from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=32)
    publish = models.CharField(max_length=32)
    author = models.CharField(max_length=32)

class phblish(models.Model):
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=32)