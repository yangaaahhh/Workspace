from haystack import indexes
from .models import Post
# 对某个 app 下的数据进行全文检索，就要在该 app 下创建一个 search_indexes.py 文件
# 然后创建一个 XXIndex 类（XX 为含有被检索数据的模型），并且继承 SearchIndex 和 Indexable


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    # 每个索引里面有且只能有一个字段为document=True，代表使用此字段的内容作为索引进行检索
    # usr_template=True，允许使用数据模板去建立搜索引擎索引的文件，即索引里面需要存放的一些东西，如post的title和body
    # 数据模板路径：templates/search/indexes/yourapp/<model_name>_text.txt
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
