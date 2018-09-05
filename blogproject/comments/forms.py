from django import forms
from .models import Comment


# 表单类需继承自forms.Form或者forms.ModelForm，当表单对应有一个数据库模型，使用ModelForm较为简单
class CommentForm(forms.ModelForm):
    class Meta:
        # 表明表单对应的数据库模型是Comment类
        model = Comment
        # fields规定的是要显示的字段
        fields = ['name', 'email', 'text']
