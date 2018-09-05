from django.conf.urls import url
from . import views

# 视图函数命名空间。告诉 Django 这个 urls.py 是属于 blog 应用的
app_name = 'blog'
urlpatterns = [
    # name 参数，作为处理函数 index 的别名
    url(r'^$', views.index, name='index'),
    # (?P<pk>[0-9]+) 表示命名捕获组，作用是从用户访问的URL里把括号内匹配的字符串捕获并作为关键字参数传给对应的视图函数
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[1-9]{1,2})/$', views.archives, name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
]
