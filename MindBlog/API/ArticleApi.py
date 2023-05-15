'''

'''

from flask.views import MethodView
from MindBlog.models import Article
from flask import request
from MindBlog.db import dbAddData

# 初始化Api
def articleApiInit(app):
    article_view = ArticleApi.as_view('article_api');
    app.add_url_rule('/articles/',defaults = {'article_id' : None}, view_func = article_view, methods = ['GET',]);
    app.add_url_rule('/articles/<int:article_id>',view_func = article_view, methods = ['GEt','PUT','DELETE']);
    app.add_url_rule('/articles/',view_func = article_view, methods = ['POST']);
    
# 文章Api
class ArticleApi(MethodView):
    
    # 处理GET请求
    def get(self, article_id):
        if article_id:      # 有传入 article_id 值
            # 查询对应 article_id 的数据
            article: Article = Article.query.get(article_id);
            
            if article:         # 查询到数据
                status = True;
                message = 'Get article data succeed.';
                result = {
                    'ArticleId' : article.ArticleId,
                    'ArticleTitle' : article.ArticleTitle,
                    'ArticleAuthor' : article.ArticleAuthor,
                    'ArticleAuthorId' : article.ArticleAuthorId,
                    'ArticleContext' : article.ArticleContext,
                    'ArticleComment' : article.ArticleComment,
                }
            else:           # 查询不到数据
                status = False;
                message = 'Could not get the id[%s] article.' %article_id;
                result = None;
        else:        # 没有传入 article_id 值
            status = False;
            message = 'please enter a article_id';
            result = None;
        
        # 返回结果
        return {
            'status' : status,
            'message' : message,
            'result' : result,
        }
    
    # 处理POST请求
    def post(self):
        # 判断数据类型，仅支持json结构。[todo：增加其他数据结构解析]
        if request.content_type.startswith('application/json'):
            rawdata = request.get_json();
        else:
            rawdata = None;
            status = False;
            message = 'please submit data with type "application/json".';
            result = None;
        # 处理数据
        if rawdata:
            art = Article();
            art.ArticleId = rawdata['ArticleId'];
            art.ArticleTitle = rawdata['ArticleTitle'];
            art.ArticleAuthor = rawdata['ArticleAuthor'];
            art.ArticleAuthorId = rawdata['ArticleAuthorId'];
            art.ArticleContext = rawdata['ArticleContext'];
            art.ArticleComment = rawdata['ArticleComment'];
            
            # 添加数据进数据库
            if dbAddData(art):
                status = True;
                message = 'add article data succeed.';
                result = 'succeed';
            else:
                status = False;
                message = 'commit article data failed.';
                result = 'failed';
        # 返回结果
        return {
            'status' : status,
            'message' : message,
            'result' : result,
        }