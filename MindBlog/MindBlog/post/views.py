from . import post
from flask import render_template,request,session,flash,redirect,url_for
from flask_login import current_user
from MindBlog.models import Article
from MindBlog.db import dbAddData,dbDeleteData,dbUpdateData
import json
from .forms import NewPostsForm,EditPostsForm
from datetime import datetime
# 查看用户所有post
@post.route('/allposts',methods=['GET','POST'])
def allposts():
    pass;

# 获取所有文章
@post.route('/all',methods=['GET'])
def all():
    # 拿到当前页面
    page = request.args.get('page',1,type=int);
    print('page %d' %page);
    # 拿到当前页面对应的文章数据
    pagination = Article.query.order_by(Article.ArticlePostDate.desc()).paginate(page=page,per_page=8,error_out=False);
    if(pagination is None):
        print('get nothing');
    posts = pagination.items;
    result = {};
    for index in range(len(posts)):
        result[str(index)] = posts[index].json();
    # 添加总共的页数
    result['pagesNumber'] = pagination.pages;
    result['postNumber'] = pagination.total;
    print(result);
    return json.dumps(result);

# 查看用户对应id的post
@post.route('/post/<int:id>',methods=['GET'])
def checkPost(id):
    post = Article.query.get(id);
    return render_template("post/postdetail.html",post=post);

@post.route('/new',methods=['GET','POST'])
def newPost():
    form = EditPostsForm();
    
    if(form.validate_on_submit()):
        art = Article(ArticleId = Article.newPostId(),
                      ArticleTitle = form.title.data,
                      ArticleContent = form.content.data,
                      ArticlePostDate = datetime.now(),
                      ArticleAuthor = current_user);
        try:
            dbAddData(art);
        except Exception as error:
            flash('保存失败。');
            print('add now post error : %s' %error);
        return redirect(url_for('auth.space',id=current_user.UserId));
    
    return render_template("post/newpost.html",form=form);
        

# 编辑对应id的post
@post.route('/edit/<int:id>',methods=['GET','POST'])
def editPost(id):
    form = NewPostsForm();
    art = Article.query.get(id);
    
    if(form.validate_on_submit()):
        art.ArticleTitle = form.title.data;
        art.ArticleContent = form.content.data;
        try:
            dbUpdateData(art);
        except Exception as error:
            flash('保存失败。');
            print('add now post error : %s' %error);
        return redirect(url_for('auth.space',id=current_user.UserId));
    if(not art):
        flash('文章不存在。');
        return redirect(url_for('auth.space',id=current_user.UserId));
    else:
        form.title.data = art.ArticleTitle;
        form.content.data = art.ArticleContent;
    
    return render_template("post/editpost.html",form=form);

# 删除对应id的post
@post.route('/delete/<int:id>',methods=['GET','Post'])
def deletePost(id):
    post = Article.query.get(id);
    dbDeleteData(post);
    flash('删除文章成功');
    return {
        'status':'success'
    }