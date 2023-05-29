'''
    [todo]
    1.cookie的有效时间设置、处理。
    2.token加上时间。
    2.完善post请求数据的发送格式支持。
'''

from flask.views import MethodView
from MindBlog.models import User
from flask import request,session,current_app,Response
from werkzeug.security import generate_password_hash,check_password_hash
import json
from MindBlog.db import dbAddData,dbUpdateData,dbDeleteData
from sqlalchemy import or_,and_,not_
from random import randint

# api白名单
from MindBlog.api.WhiteList import wlisWhiteList

# 注册userapi[同一个方法可注册多个url_rule]
def userapiInit(app):
    user_view = UserApi.as_view('user_api');
    app.add_url_rule('/users/',defaults={'userId' : None}, view_func = user_view,methods=['GET',]);
    app.add_url_rule('/users/',view_func = user_view,methods = ['POST']);
    app.add_url_rule('/users/<int:userId>', view_func = user_view, methods = ['GET','PUT','DELETE']);
    #app.add_url_rule('/users/<string:userName>', view_func = user_view, methods = ['GET','PUT','DELETE']);
    

# 生成可用随机userId
def userIdInit():
    id = randint(100000,999999);
    user: User = User.query.get(id);
    while(user):
        if(id > 100000 & id < 999999):
            id += 1;
        user: User = User.query.get(id);  
    return id;

# 生成token[todo：增加token的失效性]
import jwt
def generateToken(payload):
    key = current_app.config.get('SECRET_KEY');
    try:
        token = jwt.encode(payload,key,algorithm='HS256');
        return token;
    except Exception as error:
        print('generate token failed %s' %error);
        return error;
# 校验token  
def checkToken(token):
    key = current_app.config.get('SECRET_KEY');
    payload = jwt.decode(token,key,algorithms='HS256');
    return payload;

    
# 用户Api
class UserApi(MethodView):
    
    # 处理get请求[主要查询用户信息等操作]
    def get(self, userId):
        
        # 判断是不是白名单
        if(not wlisWhiteList()):
            return None;
        
        #是否有传username
        if not userId:
            repMsg = '请输入对应的UserID';
            status = False;
            result = None;
        else:
            user: User = User.query.get(userId);
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
            'result':result
        }
    # 第二个规则
    '''def get(self, userName):
        # 判断是不是白名单
        if(not wlisWhiteList()):
            return None;

        #是否有传username
        if not userName:
            repMsg = '请输入对应的UserID';
            status = False;
            result = None;
        else:
            user: User = User.query.filter_by(UserName=userName).first();
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
            'result': result
        }
'''
    # 处理post请求[主要用于处理用户注册]
    def post(self):
        # 是否白名单
        if(not wlisWhiteList()):
            return None;
        # 获取post原生数据
        rawdata = request.get_json();

        # 判断是登录还是注册
        if('UserName' in rawdata):
            result = self.registerPost(rawdata);            # 处理注册请求
        elif(('UserEmail' in rawdata ) or ('UserPassword' in rawdata)):
            result = self.loginPost(rawdata);               # 处理登录请求
        elif('UserLogout' in rawdata):                      # 登出处理
            session['login'] = False;
            session['user'] = None;
            return {
                'status':True,
                'message':'logout success.'
            }
        else:
            result = None;

        return result;
    
    # 处理put请求[主要用于更新用户信息]
    def put(self,userId):
        # 是否白名单
        if(not wlisWhiteList()):
            return None;
        
        # 判断是否在登录状态
        if not session['login']:
            status = False;
            message = 'please login';
        else:
            user:User = User.query.get(userId);
            # 判断用户是否存在
            if not user:
                status = False;
                message = 'user not exist.';
            else:
                if request.content_type.startswith('application/json'):
                    rawdata = request.get_json();
                else:
                    rawdata = None;
                    message = 'please summit with contentType as "application/app"';
                
                # 判断更改项
                if('UserName' in rawdata):
                        existusername = User.query.filter_by(UserName=rawdata['UserName']).first();
                if('UserEmail' in rawdata):
                        existuseremail = User.query.filter_by(UserName=rawdata['UserEmail']).first();
                if(existusername or existuseremail):
                    return {
                        'status':False,
                        'message':"email or username or you're not changing things exist."
                        };
                
                if rawdata:
                    # 判断更改项
                    if not existusername:
                        user.UserName = rawdata['UserName'];
                    if not existuseremail:
                        user.UserEmail = rawdata['UserEmail'];
                    
                    if('UserPassword' in rawdata):
                        user.UserPassword = generate_password_hash(rawdata['UserPassword']);
                    # 更新数据库数据
                    if(dbUpdateData(user)):
                        status = True;
                        message = "change user info success";
                    else:
                        status = False;
                        message = "database error.please check errorlogs";
                else:
                    status = False;
                    message = "json data error";
            
            return {
                'status':status,
                'message':message
            }
    
    # 处理delete请求
    def delete(self,userId):
        # 是否白名单
        if(not wlisWhiteList()):
            return None;
        
        # 是否登录状态
        if(not session['login']):
            return None;
        # 获取用户数据
        user: User = User.query.get(userId);
        if(user):
            if(dbDeleteData(user)):
                status = True;
                message = 'delete user success.';
                session['login'] = False;
            else:
                status = False;
                message = 'delete user failed.check error log';
        
        return {
            'status':status,
            'message':message
        }
            
    
    # 处理登录请求
    def loginPost(self,data):
        # 是否白名单
        if(not wlisWhiteList()):
            return None;
        #判断是否已登录
        if('login' in session):
            if(session['login']):
                return None;
        else:
            session['login'] = False;
        # 使用Response对象返回数据
        res = Response(status=200,content_type='application/json');
        
        if data:
            user: User=User.query.filter_by(UserEmail=data['UserEmail']).first();
            # 判断用户是否存在
            if not user:
                status = False;
                message = 'email not registered.';
                userinfo = None;
            else:
                if(check_password_hash(user.UserPassword,data['UserPassword'])):           # 检查原生密码
                    status = True;
                    message = 'login success';
                    userinfo = {
                        'UserId':user.UserId,
                        'UserName':user.UserName,
                        'UserPassword':user.UserPassword,
                        'UserEmail':user.UserEmail
                    }
                    #设置token
                    token = generateToken(userinfo);
                    res.set_cookie('token',token);
                    session['login'] = True;
                    session['user'] = user.UserId;
                else:
                    status = False;
                    message = 'password error.';
                    userinfo = None;
                    session.login = False;
        else:
            status = False;
            message = 'post error, please post data as "application/json".';
            userinfo = None;
        
        # 设置数据
        res.set_data(json.dumps({'status':status,'message':message}));
        
        return res;
    
    # 处理注册请求
    def registerPost(self,data):
                
        if data:
            # 判断邮箱和用户名是否存在
            userEmail = User.query.filter_by(UserEmail=data['UserEmail']).first();
            userName = User.query.filter_by(UserName=data['UserName']).first();
            
            # 条件处理
            if userEmail:
                status = False;
                message = "Email Exist";
            elif userName:
                status = False;
                message = "UserName Exist";
            else:
                user = User();
                user.UserId = userIdInit();
                user.UserName = data['UserName'];
                user.UserEmail = data['UserEmail'];
                user.UserPassword = generate_password_hash(data['UserPassword']);
                #新增用户
                if dbAddData(user):
                    status = True;
                    message = 'Add user succeed';
                else:
                    status = False;
                    message = 'Add user failed.check errorlog';
        else:
            status = False;
            message = 'post error, please post data as "application/json".';
        
        # 使用Response对象返回数据
        res = Response(status=200,content_type='application/json');
        res.set_data(json.dumps({'status':status,'message':message}));
           
        return res;
            
            
        