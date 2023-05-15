from MindBlog.db import g_db

# 用户字段
class User(g_db.Model):
    __tablename__ = 'User';
    UserId = g_db.Column(g_db.Integer, primary_key = True);
    UserName = g_db.Column(g_db.String(80), unique = True);
    UserEmail = g_db.Column(g_db.String(30), unique = True);
    UserPassword = g_db.Column(g_db.String(18));
    #UserPic = g_db.Column(g_db.String(32));
    
# 文章字段
class Article(g_db.Model):
    __tablename__ = 'Article';
    ArticleId = g_db.Column(g_db.Integer, primary_key = True);
    ArticleTitle = g_db.Column(g_db.String(80));    # 文章标题
    ArticleAuthor = g_db.Column(g_db.String(80));   # 文章作者
    ArticleAuthorId = g_db.Column(g_db.Integer);    # 文章作者ID
    ArticleContext = g_db.Column(g_db.Text);        # 文章内容
    ArticleComment = g_db.Column(g_db.Text);       # 文章评论
    
# 评论字段
class Comment(g_db.Model):
    __tablename__ = 'Comment';
    CommentId = g_db.Column(g_db.Integer, primary_key = True);
    CommentContext = g_db.Column(g_db.Text);        # 评论内容
    CommentUsername = g_db.Column(g_db.String(80)); # 评论用户名
    CommentTime = g_db.Column(g_db.String(24));     # 评论时间