from flask import render_template,request
from . import home
from MindBlog.models import Article

@home.route('/')
def index():
    return render_template('index.html')