'''
    [todo]
    1.完善UserApi的put、delete方法。
    2.完善post请求数据的发送格式支持。
'''

from flask.views import MethodView
from MindBlog.models import User
from flask import request
from werkzeug.security import generate_password_hash,check_password_hash
import json
from MindBlog import dbAddData

# 注册userapi
def userapiInit(app):
    user_view = UserApi.as_view('user_api');
    app.add_url_rule('/users/',defaults={'user_id' : None}, view_func = user_view,methods=['GET',]);
    app.add_url_rule('/users/',view_func = user_view,methods = ['POST']);
    app.add_url_rule('/users/<int:user_id>', view_func = user_view, methods = ['GET','PUT','DELETE']);
    
# 用户Api
class UserApi(MethodView):
    
    # 处理get请求
    def get(self, user_id):
        if not user_id:
            repMsg = '请输入对应的UserID';
            status = False;
            result = None;
        else:
            user: User = User.query.get(user_id);
            if user:
                status = True;
                repMsg = '用户查询成功';
                result = {
                    'UserId' : user.UserId,
                    'UserName' : user.UserName,
                    'UserEmail' : user.UserEmail,
                    'UserPasswrod' : user.UserPassword,
                }
            else:
                status = False;
                repMsg = '没有该用户';
                result = None;
        
        return {
            'status' : status,
            'message' : repMsg,
            'result' : result,
        }

    # 处理post请求
    def post(self):
        if request.content_type.startswith('application/json'):
            rawdata = request.get_json();
            print(rawdata);
        else:
            rawdata = None;
            repMsg = 'post error, please post as "application/json".';
            status = False;
        
        if rawdata:
            user = User();
            user.UserId = rawdata['UserId'];
            user.UserName = rawdata['UserName'];
            user.UserEmail = rawdata['UserEmail'];
            user.UserPassword = generate_password_hash(rawdata['UserPassword']);
            
            if dbAddData(user):
                status = True;
                repMsg = 'Add user succeed';
            else:
                status = False;
                repMsg = 'Add user failed.check errorlog';

        return {
            'status' : status,
            'message' : repMsg,
        }
            
            
        