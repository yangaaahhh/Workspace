from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from comments.forms import CommentForm
import markdown
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q
from django.core.paginator import Paginator
# from django.http import HttpResponse


# Create your views here.
# 主页面视图函数
def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list, })


# 主页面类视图
class IndexView(ListView):
    # 指定model为Post，即告诉Django要获取的模型是Post
    model = Post
    # 指定要渲染的模板
    template_name = 'blog/index.html'
    # 指定获取模型列表的数据保存的变量名，传递给模板
    context_object_name = 'post_list'
    # 规定一页显示3篇文章
    paginate_by = 3

    # 获取分页导航数据
    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，无需显示分页导航，不用任何导航条数据，返回空字典
            return {}
        # 当前左边连续页码
        left = []
        # 当前右边连续页码
        right = []
        # 当前页左边页码是否需要显示省略号
        left_has_more = False
        # 当前页右边页码是否需要显示省略号
        right_has_more = False
        # 是否需要显示第一页的页码，当左边连续页码包含第一页时，不需显示
        first = False
        # 是否需要显示最后一页的页码，当右边连续页码包含最后一页时，不需显示
        last = False
        # 当前请求页的页码
        page_num = page.number
        # 总页数
        total_page = paginator.num_pages
        # 获得页码列表，如4页就是[1,2,3,4]
        page_range = paginator.page_range

        if page_num == 1:
            # 第一页，则只需获取右侧页码，假如获取右边两页页码
            right = page_range[page_num:page_num + 2]
            if right[-1] < total_page - 1:
                # 如果右侧要显示页码比最后一页减一还要小，那么右侧需要显示省略号
                right_has_more = True
            if right[-1] < total_page:
                # 如果右侧要显示的最后一页页码比最后一页小，那么显示最后一页
                last = True
        elif page_num == total_page:
            # 最后一页，只需获取左边页码
            left = page_range[(page_num - 3) if (page_num - 3) > 0 else 0:page_num - 1]
            if left[0] > 2:
                # 如果左边页码列表第一页比2还大，那么显示省略号
                left_has_more = True
            if left[0] > 1:
                # 即左边页码列表第一页比1 大，那么显示第一页
                first = True
        else:
            # 用户请求的是中间的页码
            left = page_range[(page_num - 3) if (page_num - 3) > 0 else 0:page_num - 1]
            right = page_range[page_num:page_num + 2]
            if right[-1] < total_page - 1:
                right_has_more = True
            if right[-1] < total_page:
                last = True
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        date = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last
        }
        return date

    # 覆写get_context_data方法
    def get_context_data(self, **kwargs):
        # 首先获得父类生成的传递给模板的字典
        context = super(IndexView, self).get_context_data(**kwargs)
        # 在父类生成的字典中已经存在分页相关的模板变量
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        # 将分页数据更新到context中
        context.update(pagination_data)
        # 返回context，让ListView使用这个模板变量中的字典去渲染模板
        return context


# 详情页面视图函数
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()  # 阅读量+1
    post.body = markdown.markdown(post.body,
                                  extensions=
                                  ['markdown.extensions.extra',
                                   'markdown.extensions.codehilite',
                                   'markdown.extensions.toc',
                                   ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {'post': post,
               'form': form,
               'comment_list': comment_list}
    return render(request, 'blog/detail.html', context=context)


# 详情页类视图
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写get方法，每浏览一次文章，阅读数+1
        # get 方法返回的是一个HttpResponse实例
        # 当调用get方法之后，才会有 self.object 属性，为 Post 模型实例，也就是被访问的文章
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        # 覆写此方法，对 post 的 body 进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
            # slugify --> 能够很好的处理中文，结合TocExtension处理markdown的锚点
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        # 利用markdown自动生成标题
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        # post 已经通过DetailView传递给模板，然后把form表单和评论列表传递给模板
        # 在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的
        # 而在视图函数中，是通过 render 函数传递的字典 context 传递给模板
        context = super(PostDetailView, self).get_context_data(**kwargs)
        comment_list = self.object.comment_set.all()
        form = CommentForm()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context
    # get_object 和 get_context_data 在 get 方法中调用


# 归档页面视图函数
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month)
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 归档类视图
class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month)


# 分类页面视图函数
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 分类类视图
class CategoryView(IndexView):
    def get_queryset(self):
        # 在类视图中，从 URL 捕获的命名组参数值保存在实例的 kwargs 属性
        # self.kwargs.get('pk') --> 获取从URL捕获的分类pk，然后调用父类的get_queryset()获取所有文章，在筛选该分类下的文章
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


# 标签类视图
class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tag=tag)


def search(request):
    # 模板表单中name = q ,所以这里键也为 q
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    # icontains ,contains --> 包含，i --> 不区分大小写
    # Q 对象用于包装查询表达式，提供复杂的查询逻辑
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', context={'error_msg': error_msg,
                                                       'post_list': post_list})
