from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length
from wtforms import ValidationError

class NewPostsForm(FlaskForm):
    title = StringField('文章标题',validators=[DataRequired(),Length(1,64)]);
    content = TextAreaField('文章正文',validators=[DataRequired()]);
    submit = SubmitField('保存');
    
class EditPostsForm(FlaskForm):
    title = StringField('文章标题',validators=[DataRequired(),Length(1,64)]);
    content = TextAreaField('文章正文',validators=[DataRequired()]);
    submit = SubmitField('保存');
    