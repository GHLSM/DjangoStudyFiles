from app01 import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


def check_price(data):
    # 内部逻辑
    return data


class BookSer(serializers.Serializer):
    title = serializers.CharField()
    price = serializers.CharField(validators=[check_price])
    publish = serializers.CharField()

    # 想要反序列化更新数据必须自己重写update方法, 将数据对应传递
    def update(self, instance, validated_data):
        # instance是book对象
        # validated_data是校验后的数据
        instance.title = validated_data.get('title')
        instance.price = validated_data.get('price')
        instance.publish = validated_data.get('publish')
        instance.save()  # book.save()  django的orm提供的
        return instance

    # 想要反序列化新增数据必须自己重写create方法
    def create(self, validated_data):
        # models.Book.objects.create(title=...)
        instance = models.Book.objects.create(**validated_data)  # 只有数据对应才可以这样打散传入
        return instance  # 必须返回

    # 局部钩子
    def validate_price(self, data):  # 会把验证字段的数据传入,类型为字段类型，主要注意
        # 添加校验，如果价格小于十，校验不通过
        if float(data) > 10:
            return data  # 将数据返回
        else:
            raise ValidationError('价格低了')

    def validate(self, validated_data):  # validated_data内部含有所有的数据
        # 内部逻辑
        return validated_data

# class BookMolSer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Book
#         # 序列化所有字段
#         # fields = '__all__'
#         # 序列化需要的字段()\[]都可以
#         # fields = ('title', 'price')
#         # 和fields不可以同时写，代表不需要的字段
#         exclude = ('title')
