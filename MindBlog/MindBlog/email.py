from flask import Flask,current_app
from flask_mail import Mail,Message
from threading import Thread

email = Mail();

# 初始化邮箱
def emailInit(app):
    # 初始化邮箱
    #配置邮件：服务器|端口|传输层安全协议|邮箱名|身份认证密码（授权码）
    app.config.update(
        MAIL_SERVER="smtp.163.com",
        MAIL_PORT=465,
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=True,
        MAIL_USERNAME="jimmylooun@163.com",
        MAIL_PASSWORD="MOJGAHIMQMUYACUX"
    )
    email.init_app(app);

# 发送邮件[base function]
def send_async_email(app,msg):
    with app.app_context():
        email.send(msg);

# 发送邮件
def send_email(recive,body):
    msg = Message(body,sender=current_app.config['MAIL_USERNAME'],recipients=[recive]);
    thr = Thread(target=send_async_email,args=[current_app,body]);
    thr.start()
    return thr;

# 同步发送邮件
def send_dirct_email(recive,title,message):
    msg = Message(title,sender="jimmylooun@163.com",recipients=[recive]);
 
    # 邮件内容
    msg.body = message;
    if email.send(msg):
        return True;
    else:
        return False;
    
 