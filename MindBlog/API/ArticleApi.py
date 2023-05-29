'''
todo：

'''

from flask.views import MethodView
from flask import request,session,current_app,Response
from random import randint
import json

# 文章模型
from MindBlog.models import Article
# 白名单
from MindBlog.api.WhiteList import wlisWhiteList
# 数据库增、删、改
from MindBlog.db import dbAddData,dbDeleteData,dbUpdateData
# 用户
from MindBlog.models import User

# 初始化Api
def articleApiInit(app):
    article_view = ArticleApi.as_view('article_api');
    app.add_url_rule('/articles/',defaults = {'articleId' : None}, view_func = article_view, methods = ['GET',]);
    app.add_url_rule('/articles/<int:articleId>',view_func = article_view, methods = ['GEt','PUT','DELETE']);
    app.add_url_rule('/articles/',view_func = article_view, methods = ['POST']);

# 生成可用随机articleId
def articleIdInit():
    id = randint(100000,999999);
    article :  Article = Article.query.get(id);
    while(article):
        if(id > 100000 & id < 999999):
            id += 1;
        article :  Article = Article.query.get(id);
    return id;

# 处理未登录get请求
def getNotArticleId():
    #没有articleId的话，就返回所有的文章
    article: Article = Article.query.all();
    res = Response(status=200,content_type='application/json');
    data = {};
    
    for index in range(len(article)):
        data['data'+ str(index)] = {
            'ArticleId':article[index].ArticleId,
            'ArticleTitle':article[index].ArticleTitle,
            'ArticleAuthor':article[index].ArticleAuthor.UserId,
            'ArticleContent':article[index].ArticleContent,
            'ArticlePostDate':article[index].ArticlePostDate
        }
        if(index == 10):
            break;
    
    res.set_data(json.dumps(data));
    
    return res;
# 处理有articleId的get请求
def getWithArticleId(id):
    # 查询对应 articleId 的数据
    article: Article = Article.query.get(id);
    # reponse
    rep = Response(status=200,content_type='application/json');   
    if article:         # 查询到数据
        status = True;
        message = 'Get article data succeed.';
        result = {
            'ArticleId' : article.ArticleId,
            'ArticleTitle' : article.ArticleTitle,
            'ArticleAuthor' : article.ArticleAuthor.UserId,
            'ArticleContent' : article.ArticleContent,
            'ArticleRead':article.ArticleRead,
            'ArticlePostDate':article.ArticlePostDate
        }
        rep.set_data(json.dumps(result));
    else:           # 查询不到数据
        status = False;
        message = 'Could not get the id[%s] article.' %id;
    
    return rep;
    
    
 
# 文章Api
class ArticleApi(MethodView):
    
    # 处理GET请求
    # 分有无ariticleId的情况
    def get(self, articleId):
        # 判断是否白名单
        if(not wlisWhiteList()):
            return None;
        
        if articleId:      # 有传入 articleId 值
            rep = getWithArticleId(articleId);
        else:
            rep =getNotArticleId();
        
        # 返回结果
        return rep;
    
    # 处理POST请求
    def post(self):
        # 判断是否白名单
        if(not wlisWhiteList()):
            return None;
        
        # 判断是否登录
        print('login is %s ' %str(session['login']))
        if(not session['login']):
            return None;
        
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
            art.ArticleId = articleIdInit();
            art.ArticleTitle = rawdata['ArticleTitle'];
            art.ArticleContent = rawdata['ArticleContent'];
            art.ArticlePostDate = rawdata['ArticlePostDate'];
            
            art.ArticleAuthor = User.query.get(session['user']);
            
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
    
    # 处理put请求
    def put(self,articleId):
        #判断白名单
        if(not wlisWhiteList()):
            return None;
        
        # 判断登录状态
        if(not session['login']):
            return None;
        # 获取原生数据
        if(request.content_type.startswith('application/json')):
            rawdata = request.get_json();
        else:
            return None;
        
        article:Article = Article.query.get(articleId);
        # 判断作者是否当前登录用户
        if(article.ArticleAuthor.UserId != session['user']):
            return None;
        else:
            if('ArticleTitle' in rawdata):
                article.ArticleTitle = rawdata['ArticleTitle'];
            if('ArticleContent' in rawdata):
                article.ArticleContent = rawdata['ArticleContent'];
            if('ArticleContent' in rawdata):
                article.ArticlePostDate = rawdata['ArticlePostDate'];
            
            if(dbUpdateData(article)):
                rep = Response(status=200,content_type='application/json');
                rep.set_data(json.dumps({'status':True,'message':'update article success.'}));
                return rep;
            else:
                return None;
    
    # 处理delete请求
    def delete(self,articleId):
        #判断白名单
        if(not wlisWhiteList()):
            return None;
        
        # 判断登录状态
        if(not session['login']):
            return None;
        article:Article = Article.query.get(articleId);
        # 判断作者是否当前登录用户
        if(article.ArticleAuthor.UserId != session['user']):
            return None;
        else:
            if(dbDeleteData(article)):
                rep = Response(status=200,content_type='application/json');
                rep.set_data(json.dumps({'status':True,'message':'delete article success.'}));
                return rep;
            else:
                return None;
        