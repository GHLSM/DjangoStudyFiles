from django import template
from app01 import models
from django.db.models import Count
from django.db.models.functions import TruncMonth

register = template.Library()


# 自定义inclusion_tag


@register.inclusion_tag('left_menu.html')
def left_menu(username):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    blog = user_obj.blog

    category_list = models.Category.objects.filter(blog=blog).annotate(count_num=Count('article__pk')).values('name',
                                                                                                              'count_num',
                                                                                                              'pk')
    tag_list = models.Tag.objects.filter(blog=blog).annotate(count_num=Count('article__pk')).values('name', 'count_num',
                                                                                                    'pk')
    time_list = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth('create_time')).values(
        'month').annotate(count_num=Count('pk')).values('month', 'count_num')
    # print(time_list)
    return locals()
