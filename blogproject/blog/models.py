from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_time = models.DateTimeField()
    # 最后一次修改时间
    modified_time = models.DateTimeField()
    # 摘要，blank=True 允许该字段为空
    excerpt = models.CharField(max_length=200, blank=True)
    # 一对多关系
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # 多对多关系
    tag = models.ManyToManyField(Tag, blank=True)
    # django.contrib.auth 是 Django 内置应用，专门处理网站用户的注册、登录等流程，User 是 Django 已经写好的用户模型
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # 自定义方法
    # 首先找到 blog 应用下的 detail 视图函数，然后 reverse 函数会去解析 detail 对应的URL
    # 此时对应的 URl 规则是 post/(?P<pk>[0-9]+)/ 正则表达式，正则表达式后面部分会被传入的参数 pk 所替换
    # 例如 post.pk 是 24，URL 就为 post/24/
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
