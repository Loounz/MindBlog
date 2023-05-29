from . import auth
from flask import render_template,redirect,request,url_for,flash,session
from flask_login import login_user,logout_user,login_required,current_user
from MindBlog.auth.forms import LoginForm,RegisterForm,ChangeUserEmailForm,ChangeUserNameForm,ChangePasswordFrom
from MindBlog.models import User,Article
from MindBlog.db import dbAddData,dbUpdateData,dbDeleteData
from datetime import datetime

# 登录
@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm();
    if form.validate_on_submit():
        user = User.query.filter_by(UserEmail=form.email.data.lower()).first();
        if user and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data);
            next = request.args.get('next');
            if next is None or not next.startswith('/'):
                next = url_for('home.index');
            return redirect(next);
        flash('邮箱或者密码错误.');
    return render_template('auth/login.html',form=form);

# 登出
@auth.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user();
    flash('登出成功。');
    return redirect(url_for('home.index'));

# 注册
@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm();
    
    if form.validate_on_submit():
        # 判断验证码是否正确
        if(isCodeValid('register',int(form.code.data),str(form.email.data))):
            user = User(UserEmail=form.email.data.lower(),
                        UserName=form.username.data,
                        password=form.password.data);
            dbAddData(user);            # 写入数据库
            flash('注册成功');
            session.pop('register');    # 清除验证码
            return redirect(url_for('auth.login'));
        else:
            flash('验证码错误/验证码过期,请检查验证码或者重新获取');
        
    return render_template('auth/register.html',form=form);

# 修改密码
@auth.route('/changepassword',methods=['GET','POST'])
def changepassword():
    form = ChangePasswordFrom();
    # 判断提交信息是否全 & 验证码是否有效
    if form.validate_on_submit():
        if isCodeValid('changepassword',int(form.code.data),str(form.email.data)):
            # 清除验证码
            session.pop('changepassword');
            # 登出
            if(current_user.is_authenticated):
                current_user.reset_password(form.newpassword.data);
                dbUpdateData(current_user);
                logout_user();
            else:
                user=User.query.filter_by(UserEmail=form.email.data).first();
                user.reset_password(newpassword = form.newpassword.data);
                dbUpdateData(user);
            return redirect(url_for('auth.login'));
    
    return render_template('auth/changepassword.html',form=form);


# 修改用户信息
@auth.route('/changeinfo',methods=['GET','POST'])
def changeinfo():
    emailform = ChangeUserEmailForm();
    nameform = ChangeUserNameForm();
    
    # 修改邮箱
    if emailform.validate(extra_validators=None) and emailform.submit2.data:
        if(isCodeValid('changeemail',emailform.code.data,emailform.email.data)):
            current_user.UserEmail = emailform.email.data.lower();
            dbUpdateData(current_user);
            session.pop('changeemail');
        
            next = request.args.get('next');
            if next is None or not next.startswith('/'):
                next = url_for('home.index');
            return redirect(next);
        else:
            flash('修改邮箱失败，验证码错误/过期');
        
    # 修改用户名
    if nameform.validate() and nameform.submit1.data:
        current_user.UserName = nameform.username.data;
        dbUpdateData(current_user);
        flash('修改用户名成功')
    
    # 处理get请求
    nameform.username.data = current_user.UserName;
    emailform.email.data = current_user.UserEmail;
    
    context = {
        'emailform':emailform,
        'nameform':nameform
    }
    
    return render_template('auth/changeinfo.html',**context);

# 用户空间
@auth.route('/<id>/space',methods=['GET','POST'])
def space(id):
    posts:Article = Article.query.filter_by(ArticleAuthor = current_user).order_by(Article.ArticlePostDate.desc());
    # 获取成功后，直接渲染模板
    return render_template('post/postmanage.html',posts=posts);

# 获取验证码
from MindBlog.email import send_email,send_dirct_email
@auth.route('/code',methods=['GET'])
def getCode():
    # 获取请求类型
    types = request.args.get('type');
    email = request.args.get('email');      # 获取email
    
    # 发送注册的验证码
    if('register' == types.strip()):
        code = codeGenerate(types,email);
        title = "注册 MindBlog 账号"
        msg = "你正在注册MindBlog，验证码："+str(code)+" 有效期：5分钟";
        email = request.args.get('email');
        if send_dirct_email(str(email),title,msg):
            result = {'status':'success'};
        else:
            result = {'status':'success'};

        return result;
    # 发送修改密码的验证码
    if('changepassword' == types.strip()):
        code = codeGenerate(types,email);
        title = "修改/找回MindBlog密码"
        msg = "你正在 修改/找回 MindBlog密码，验证码："+str(code)+" 有效期：5分钟";
        email = request.args.get('email');
        if send_dirct_email(str(email),title,msg):
            result = {'status':'success'};
        else:
            result = {'status':'success'};
            
        return result;
    
    # 修改邮箱的验证码
    if('changeemail' == types.strip()):
        code = codeGenerate(types,email);
        title = "修改MindBlog账号邮箱"
        msg = "你正在 修改 MindBlog账号邮箱，验证码："+str(code)+" 有效期：5分钟";
        email = request.args.get('email');
        if send_dirct_email(str(email),title,msg):
            result = {'status':'success'};
        else:
            result = {'status':'success'};
            
        return result;
    
    return {'status':'failed'};

# 生成6位数验证码
from random import randint
def codeGenerate(type,email):
    id = randint(100000,999999); 
    # 保存到session
    session[str(type)]={
        "email":str(email),
        "code":id,
        "timestamp":int(datetime.timestamp(datetime.now())),
        "valid":600
    }
    return id;

# 验证码是否有效
def isCodeValid(types,code,email):
    data = session.get(str(types))
    print(data);
    if(data):
        if(data.get('code') == int(code)):
            if(data.get('email') == email):
                if((data.get('timestamp')+ data.get('valid')) > int(datetime.timestamp(datetime.now()))):
                    return True;
                else:
                    session.pop(str(types));    # 删除过期二维码
                    return False;
            else:
                return False;
        else:
            print('here')
            return False;
    else:
        return False;

        

