from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count

register = template.Library()


# 最新文章标签
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]


# 归档标签
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


# 分类标签
@register.simple_tag
def get_categories():
    # return Category.objects.all()
    # annotate 返回数据库中全部Category记录，同时可以做其他的事情
    # 通过Count方法，统计返回的Category记录的集合中每条记录下的文章数，接收一个和Category相关联的模型参数名
    # 通过filter() 过滤掉，分类下文章数为 0 的分类，使不显示。gt --> 大于，gte --> 大于等于
    # num_posts --> 传递到模板中的文章数
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


# 标签云标签
@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
