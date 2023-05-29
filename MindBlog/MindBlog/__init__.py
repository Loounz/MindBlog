from flask import Flask
from MindBlog.db import *
from flask_cors import CORS
from flask_bootstrap import Bootstrap4
from flask_moment import Moment
from flask_login import LoginManager
from MindBlog.models import User
from MindBlog.email import email,emailInit
from MindBlog.fakedata import fakeUsers,fakeArticles,fakeArticlesforUser
import click



moment = Moment();
login_manager = LoginManager();
login_manager.login_view = 'auth.login';

# 使用flask_login进行用户管理时，要加载用户数据
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id));


def create_app():
    app = Flask(__name__);
    app.config.from_pyfile('setting.py');
    # 跨域问题
    CORS().init_app(app);
    
    # 初始化数据库
    with app.app_context():
        dbInit(app);
        bootstrap = Bootstrap4(app);
        moment.init_app(app);
        login_manager.init_app(app);
        emailInit(app);
        
    '''
    # 初始化 userApi
    userapiInit(app);
    # 初始化 articleApi
    articleApiInit(app);
    # 初始化 commentApi
    commentApiInit(app);
    '''
    # 生成虚拟数据
    @app.cli.command('fakedata')
    @click.argument("user")
    def fake(user=None):
        '''fake 30 users & 10 posts data.'''
        if not user:
            fakeUsers(30);
            fakeArticles(10);
        else:
            fakeArticlesforUser(user);

    
    # 注册首页蓝图
    from MindBlog.home import home
    app.register_blueprint(home);
    
    # 注册author蓝图
    from MindBlog.auth import auth
    app.register_blueprint(auth);
    
    # 注册post蓝图
    from MindBlog.post import post
    app.register_blueprint(post);
    
    return app;
