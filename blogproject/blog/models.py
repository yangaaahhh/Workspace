from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags


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
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    # 自定义方法
    # 首先找到 blog 应用下的 detail 视图函数，然后 reverse 函数会去解析 detail 对应的URL
    # 此时对应的 URl 规则是 post/(?P<pk>[0-9]+)/ 正则表达式，正则表达式后面部分会被传入的参数 pk 所替换
    # 例如 post.pk 是 24，URL 就为 post/24/
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 阅读量自增
    def increase_views(self):
        self.views += 1
        # update_fields 规定只更新的字段，提高效率
        self.save(update_fields=['views'])

    # 自动生成摘要
    def save(self, *args, **kwargs):
        if not self.excerpt:
            # 实例化一个markdown对象，用于渲染body的文本
            md = markdown.Markdown(extensionns=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将Marrkdown文本渲染成html文本，然后通过strip_tags方法去掉HTML标签，截取前54个字符
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        # 调用父类save()方法
        super(Post, self).save(*args, **kwargs)

    # 通过定义内部类，指定获取的文章排列方式，可以去掉视图函数中获取文章列表时重复的排序代码
    class Meta:
        ordering = ['-created_time']
