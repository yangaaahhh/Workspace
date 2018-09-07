from django.conf.urls import url
from . import views

# 视图函数命名空间。告诉 Django 这个 urls.py 是属于 blog 应用的
app_name = 'blog'
urlpatterns = [
    # name 参数，作为处理函数 index 的别名
    # url(r'^$', views.index, name='index'),
    # 修改URL，调用类视图的as_view()方法，
    url(r'^$', views.IndexView.as_view(), name='index'),
    # (?P<pk>[0-9]+) 表示命名捕获组，作用是从用户访问的URL里把括号内匹配的字符串捕获并作为关键字参数传给对应的视图函数
    # url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    # url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[1-9]{1,2})/$', views.archives, name='archives'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    # url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
]
