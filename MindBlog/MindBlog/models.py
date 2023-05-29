from MindBlog.db import g_db
from werkzeug.security import generate_password_hash,check_password_hash
from flask import current_app
from flask_login import UserMixin
from datetime import datetime
from random import randint

# 角色字段【用于分配不同的权限】
class Role(g_db.Model):
    __tablename__ = 'Role';
    id = g_db.Column(g_db.Integer,primary_key=True);
    name = g_db.Column(g_db.String(64),unique=True);
    user = g_db.relationship('User',back_populates='role',lazy='dynamic');
    

# 用户字段
class User(UserMixin,g_db.Model):
    __tablename__ = 'User';
    UserId = g_db.Column(g_db.Integer, primary_key = True);
    UserName = g_db.Column(g_db.String(80), unique = True);
    UserEmail = g_db.Column(g_db.String(30), unique = True);
    UserPassword = g_db.Column(g_db.String(18));
    #UserPic = g_db.Column(g_db.String(32));
    
    Articles = g_db.relationship('Article',back_populates='ArticleAuthor')
    
    # role
    role_id = g_db.Column(g_db.Integer,g_db.ForeignKey('Role.id'));
    role = g_db.relationship('Role',back_populates='user');
    
    #密码不可读
    @property
    def password(self):
        raise AttributeError('用户密码不可读。');
    # 生成hash密码
    @password.setter
    def password(self,password):
        self.UserPassword = generate_password_hash(password);
    # 验证密码
    def verify_password(self,password):
        return check_password_hash(self.UserPassword,password);
    # 重载 login_user 的 get_id()函数
    def get_id(self):
        return self.UserId;
    # 重设密码
    def reset_password(self,newpassword):
        self.UserPassword = generate_password_hash(newpassword);
    # 生成可用随机userId
    @staticmethod
    def newUserId():
        id = randint(100000,999999);
        user: User = User.query.get(id);
        while(user):
            if(id > 100000 & id < 999999):
                id += 1;
            user: User = User.query.get(id);  
        return id;

    
    
    
# 文章字段
class Article(g_db.Model):
    __tablename__ = 'Article';
    ArticleId = g_db.Column(g_db.Integer, primary_key = True);
    ArticleTitle = g_db.Column(g_db.String(80));    # 文章标题
    ArticleContent = g_db.Column(g_db.Text);        # 文章内容
    ArticleRead = g_db.Column(g_db.Integer);        # 文章浏览量
    ArticlePostDate = g_db.Column(g_db.DateTime,index=True,default=datetime.utcnow()); # 文章发布时间
    
    ArticleAuthorId = g_db.Column(g_db.Integer,g_db.ForeignKey('User.UserId'));    # 文章作者ID
    ArticleAuthor = g_db.relationship('User',back_populates='Articles');   # 文章作者
    
    ArticleComment = g_db.Column(g_db.Text);       # 文章评论
    
    # 生成可用随机articleId
    @staticmethod
    def newPostId():
        id = randint(100000,999999);
        user: Article = Article.query.get(id);
        while(user):
            if(id > 100000 & id < 999999):
                id += 1;
            user: Article = Article.query.get(id);  
        return id;
    # 生成将属性转换成字典数据
    def json(self):
        return {
            'ArticleId':self.ArticleId,
            'ArticleTitle':self.ArticleTitle,
            'ArticleAuthor':self.ArticleAuthor.UserName,
            'ArticleContent':self.ArticleContent,
            'ArticleRead':self.ArticleRead,
            'ArticlePostDate':self.ArticlePostDate.strftime("%Y/%m/%d-%H%M%S")
        }
    
# 评论字段
class Comment(g_db.Model):
    __tablename__ = 'Comment';
    CommentId = g_db.Column(g_db.Integer, primary_key = True);
    CommentContext = g_db.Column(g_db.Text);        # 评论内容
    CommentUsername = g_db.Column(g_db.String(80)); # 评论用户名
    CommentTime = g_db.Column(g_db.String(24));     # 评论时间