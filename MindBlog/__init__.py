from flask import Flask
from MindBlog.db import *
from flask_cors import CORS

from MindBlog.API.UserApi import userapiInit

def create_app():
    app = Flask(__name__);
    app.config.from_pyfile('setting.py');
    # 跨域问题
    CORS().init_app(app);
    
    # 初始化数据库
    with app.app_context():
        dbInit(app);
    
    # 初始化 userApi
    userapiInit(app);
    
    # 注册测试蓝图
    
    return app;