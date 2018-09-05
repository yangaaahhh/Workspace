from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm


# Create your views here.
def post_comment(request, post_pk):
    # 首先要获取文章
    post = get_object_or_404(Post, pk=post_pk)

    # 判断http请求是POST还是GET，一般表单提交数据都是POST请求
    if request.method == 'POST':
        # 提交的数据存在request.POST中，为类字典数据，通过这个数据实例化表单类
        form = CommentForm(request.POST)

        # form.is_avlid()，检查数据是否合法
        if form.is_valid():
            # 先利用表单数据生成Comment类的实例，并且不保存到数据库
            comment = form.save(commit=False)
            # 将评论与Post绑定
            comment.post = post
            # 保存到数据库
            comment.save()
            # 重定向到文章，redirect()接受一个模型实例时，会调用这个模型实例的get_absolute_url方法，重定向到返回的URL
            return redirect(post)
        else:
            # 数据不合法，重新渲染，并且渲染表单的错误
            # 所以传给模板变量有三个：post，form， comment_list
            # post.comment_set.all() --> 反向查询全部评论
            comment_list = post.comment_set.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list}
            return render(request, 'blog/detail.html', context=context)
    # 不是POST请求，代表没有提交表单
    return redirect(post)
