'''

'''

from flask.views import MethodView
from MindBlog.models import Article

# 初始化Api
def articleApiInit(app):
    article_view = CommentApi.as_view('article_api');
    app.add_url_rule('/articles/',defaults = {'article_id' : None}, view_func = article_view, methods = ['GET',]);
    app.add_url_rule('/articles/<int:comment_id>',view_func = article_view, methods = ['GEt','PUT','DELETE']);
    app.add_url_rule('/articles/',view_func = article_view, methods = ['POST']);
    
# 文章Api
class ArticleApi(MethodView):
    def get(self, article_id):
        pass;
    
    def post(self):
        pass;