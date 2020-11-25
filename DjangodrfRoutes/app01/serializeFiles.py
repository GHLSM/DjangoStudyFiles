from rest_framework import serializers
from app01 import models


class BookSer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'