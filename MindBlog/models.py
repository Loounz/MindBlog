from MindBlog.db import db

# 用户字段
class User(db.Model):
    __tablename__ = 'User';
    UserId = db.Column(db.Integer, primary_key = True);
    UserName = db.Column(db.String(80), unique = True);
    UserEmail = db.Column(db.String(30), unique = True);
    UserPassword = db.Column(db.String(18));
    #UserPic = db.Column(db.String(32));
    
# 文章字段
class Article(db.Model):
    __tablename__ = 'Article';
    ArticleId = db.Column(db.Integer, primary_key = True);
    ArticleTitle = db.Column(db.String(80));    # 文章标题
    ArticleAuthor = db.Column(db.String(80));   # 文章作者
    ArticleAuthorId = db.Column(db.Integer);    # 文章作者ID
    ArticleContext = db.Column(db.Text);        # 文章内容
    ArticleComment = db.Column(db.Text);       # 文章评论
    
# 评论字段
class Comment(db.Model):
    __tablename__ = 'Comment';
    CommentId = db.Column(db.Integer, primary_key = True);
    CommentContext = db.Column(db.Text);        # 评论内容
    CommentUsername = db.Column(db.String(80)); # 评论用户名
    CommentTime = db.Column(db.String(24));     # 评论时间