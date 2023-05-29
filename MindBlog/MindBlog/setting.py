import os
# 数据库配置
url = 'sqlite:///'+os.getcwd()+'/MindBlog.db';
# 替换成linux路径
url = '/'.join(url.split('\\'));
SQLALCHEMY_DATABASE_URI = url;

# 环境变量
FLASK_APP = 'MindBlog';
FLASK_ENV = 'development';
SECRET_KEY = 'TPmi4aLWRbyVq8zu9v82dWYW1';