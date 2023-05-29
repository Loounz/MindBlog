from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from MindBlog.models import User

from flask_login import current_user

# 登录表单
class LoginForm(FlaskForm):
    email = StringField('邮箱',validators=[DataRequired(),Length(1,64),Email()]);
    password = PasswordField('密码',validators=[DataRequired()]);
    remember_me = BooleanField('记住我');
    Submit = SubmitField('登录');

# 注册信息表单 
class RegisterForm(FlaskForm):
    email = StringField('邮箱',validators=[DataRequired(),Length(1,64),Email()],id="regis-email");
    username = StringField('用户名',validators=[DataRequired(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')]);
    code = StringField('验证码',validators=[DataRequired(),Length(6)]);
    password = PasswordField('密码',validators=[DataRequired(),EqualTo('password2',message='两次密码必须相同')]);
    password2 = PasswordField('确认密码',validators=[DataRequired()]);
    submit = SubmitField('注册');
    
    # 判断邮箱是否已注册
    def validate_email(self,field):
        if User.query.filter_by(UserEmail=field.data.lower()).first():
            raise ValidationError('邮箱已注册。');
    
    # 判断用户名是否已注册
    def validate_username(self,field):
        if User.query.filter_by(UserName=field.data.lower()).first():
            raise ValidationError('用户名已注册。');

# 修改用户邮箱信息
class ChangeUserEmailForm(FlaskForm):
    email = StringField('邮箱',validators=[DataRequired(),Length(1,64),Email()],id="change-email");
    code = StringField('验证码',validators=[DataRequired(),Length(6)]);
    submit2 = SubmitField('修改');
    
    # 判断邮箱是否已注册
    def validate_email(self,field):
        if User.query.filter_by(UserEmail=field.data.lower()).first():
            raise ValidationError('邮箱已注册。');
    
    
# 修改用户名
class ChangeUserNameForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                            '用户名仅支持字母、数字以及下划线_')]);
    submit1 = SubmitField('修改');
    
    # 判断用户名是否已存在
    def validate_username(self,field):
        if User.query.filter_by(UserName = field.data).first():
            raise ValidationError('用户名 %s 已存在，请换一个。' %field.data);
    
# 修改用户密码
class ChangePasswordFrom(FlaskForm):
    email = StringField('邮箱',validators=[DataRequired(),Length(1,64),Email()],id="ch-email");
    code = StringField('验证码',validators=[DataRequired(),Length(6)]);
    newpassword = PasswordField('新密码',validators=[DataRequired(),Length(1,16)]);
    submit = SubmitField('修改');