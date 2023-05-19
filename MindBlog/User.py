'''
说明：处理用户相关的功能。
'''

from MindBlog.models import User,Article,Comment
from werkzeug.security import generate_password_hash,check_password_hash
from flask import g,session
from MindBlog.db import dbAddData,dbUpdateData,dbDeleteData

# 处理用户登录
def userLogin(userobj):
    # 根据用户email查询数据库中的数据
    user : User = User.query.get(userobj.UserEmail);
    #检查密码是否正确
    if user:
        realpassword = check_password_hash(user.UserPassword);
        if realpassword == userobj.UserPassword:
            session['login'] = True;
            session.user = user;
            result = True;
            message = "登录成功"
        else:
            session['login'] = False;
            result = False;
            message = "密码错误"
    else:
        session['login'] = False;
        result = False;
        message = "该邮箱未注册。"
        
    return {
        'result' : result,
        'message' : message
    }
    
# 处理注册
def userRegister(userobj):
    # 查询emai是否已注册
    user : User = User.query.get(userobj.UserEmail);
    if user:
        result = False;
        message = "该邮箱已注册。";
    
    # 查询用户名是否已注册
    user : User = User.query.get(userobj.UserName);
    if user:
        result = False;
        message = "该名称已注册";
    
    # 添加用户信息进数据库
    if dbAddData(userobj):
        result = True;
        message = "注册成功。"
    
    return {
        'result' : result,
        'message' : message
    }

# 修改用户信息
def userChange(userobj):
    if not session['login']:
        result = False;
        message = "请先登录，再修改用户信息。";
    else:
        if dbUpdateData(userobj):
            result = True;
            message = "更新用户信息成功。";
        else:
            result = False;
            message = "更新用户信息失败";
            
    return {
        'result' : result,
        'message' : message
    }
    
# 注销用户信息
def userDelete(userobj):
    if not session['login']:
        result = False;
        message = "请先登录，再删除用户信息。";
    else:
        if dbDeleteData(userobj):
            result = True;
            message = "删除用户信息成功。";
        else:
            result = False;
            message = "删除用户信息失败。";
    
    return {
        'result' : result,
        'message' : message
    }
    
# 登出用户
def userLogout():
    if session['login']:
        result = True;
        message = "登出成功。";
        session.clear();
    else:
        result = False;
        message = "登出失败。";
    
    return {
        'result' : result,
        'message' : message
    }
        
    
# 新增文章
def newArticle(articleobj):
    # 判断是否已登录
    if not session['login']:
        result = False;
        message = "未登录，请登录后再操作。";
    else:
        if dbAddData(articleobj):
            result = True;
            message = "文章发布成功！";
        else:
            result = False;
            message = "文章发布失败！";
    
    return {
        'result' : result,
        'message' : message
    }
    
# 修改文章
def editArticle(articleobj):
        # 判断是否已登录
    if not session['login']:
        result = False;
        message = "未登录，请登录后再操作。";
    else:
        if dbUpdateData(articleobj):
            result = True;
            message = "文章发布成功！";
        else:
            result = False;
            message = "文章发布失败！";
    
    return {
        'result' : result,
        'message' : message
    }
    
# 删除文章
def deleteArticle(articleobj):
    # 判断是否已登录
    if not session['login']:
        result = False;
        message = "未登录，请登录后再操作。";
    else:
        if dbDeleteData(articleobj):
            result = True;
            message = "文章删除成功.";
        else:
            result = False;
            message = "文章删除失败。";
            
    return {
        'result' : result,
        'message' : message
    }