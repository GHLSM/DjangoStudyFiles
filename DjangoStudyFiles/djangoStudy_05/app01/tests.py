from django.test import TestCase
import os


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoStudy_05.settings")

    import django
    django.setup()
    from app01 import models
    # models.User.objects.create(name="gh", password="123", age=23)
    #
    # user_obj = models.User(name="lsm", password="lsmagh", age=23)
    # models.User.save(user_obj)

    # user_obj = models.User.objects.filter(pk=2).first() # 数据不存在返回空
    # user_obj = models.User.objects.get(pk=2).first()  # 不建议使用，因为数据不存在报错
    # print(user_obj.name)
    # user_onj = models.User.objects.all()[2]
    # print(user_onj.name)

    # models.User.objects.filter(pk=2).update(name="ll", password="132", age=23)

    # 去重  对原表不生效
    # res = models.User.objects.all().distinct() # 去重不生效，id字段
    # res = models.User.objects.values("name", "age").distinct()
    # print(res)

    # 排序 order_by
    # res = models.User.objects.order_by("age") # 升序
    # res = models.User.objects.order_by("-age") # 降序

    # 反转reverse,反转的前提是数据已经排序了
    # res = models.User.objects.all()
    # res = models.User.objects.reverse()
    # print(res)   # 得到的数据是相同的
    # res = models.User.objects.all()
    # res = models.User.objects.order_by("age").reverse()

    # 计数
    # res = models.User.objects.count()
    # print(res)

    # 把什么排除在外获得结果 exclude
    # res = models.User.objects.exclude(name="gh")
    # print(res)

    # exists()  看数据书否存在,基本用不到,因为数据本身自带布尔值

    # 神奇的双下划线查询
    # 1.年龄大于35的数据
    # res = models.User.objects.filter(age__gt=23)
    # 2.年龄小于35的数据
    # res = models.User.objects.filter(age__lt=23)
    # 3.年龄大于等于多少
    # res = models.User.objects.filter(age__gte=23)
    # 4.年龄小于等于多少
    # res = models.User.objects.filter(age__lte=23)
    # 5.年龄为18或者23的
    # res = models.User.objects.filter(age__in=[18, 32])
    # 6.年龄再18到23的   闭区间，首尾都要
    # res = models.User.objects.filter(age__range=[18, 30])
    # 7.查询出名字里面含有n的数据   区分大小写
    # res = models.User.objects.filter(name__contains="n")
    # print(res)
    # 8.查询出名字里面含有n的数据   不区分大小写
    # res = models.User.objects.filter(name__icontains="n")
    # print(res)



