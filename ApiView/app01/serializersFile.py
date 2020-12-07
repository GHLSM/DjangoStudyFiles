from rest_framework.generics import GenericAPIView
from rest_framework import serializers
from app01 import models


class BooksSer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'
