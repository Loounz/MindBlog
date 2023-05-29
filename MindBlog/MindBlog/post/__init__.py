from flask import Flask,Blueprint,request,session

post = Blueprint('post',__name__);

from . import views
