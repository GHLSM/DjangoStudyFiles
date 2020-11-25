from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=32)
    # price = models.FloatField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    publish = models.CharField(max_length=32)
