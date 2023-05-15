'''

'''

from flask.views import MethodView
from MindBlog.models import Comment
from MindBlog.db import dbAddData

from flask import request

# 初始化Api
def commentApiInit(app):
    comment_view = CommentApi.as_view('comment_api');
    app.add_url_rule('/comments/',defaults = {'comment_id' : None}, view_func = comment_view, methods = ['GET',]);
    app.add_url_rule('/comments/<int:comment_id>',view_func = comment_view, methods = ['GEt','PUT','DELETE']);
    app.add_url_rule('/comments/',view_func = comment_view, methods = ['POST']);
    
# 评论Api
class CommentApi(MethodView):
    def get(self, comment_id):
        if comment_id:
            comment : Comment = Comment.query.get(comment_id);
            
            if comment:
                status = True;
                message = 'get comment succeed';
                result = {
                    'CommentId' : comment.CommentId,
                    'CommentContext' : comment.CommentContext,
                    'CommentUsername' : comment.CommentUsername,
                    'CommentTime' : comment.CommentTime
                };
            else:
                status = False;
                message = 'get comment failed';
                result = None;
        else:
            status = False;
            message = 'please enter a comment_id';
            result = None;
        
        return {
            'status' : status,
            'message' : message,
            'result' : result
        }
    
    def post(self):
        if request.content_type.startswith('application/json'):
            rawdata = request.get_json();
        else:
            rawdata = None;
            status = False;
            message = 'please commit data with type "application/json".';
        
        if rawdata:
            comment = Comment();
            
            comment.CommentId = rawdata['CommentId'];
            comment.CommentContext = rawdata['CommentContext'];
            comment.CommentUsername = rawdata['CommentUsername'];
            comment.CommentTime = rawdata['CommentTime'];
            
            if dbAddData(comment):
                status = True;
                message = 'commit comment data succeed.';
                result = None;
            else:
                status = False;
                message = 'commit comment data failed';
                result = None;
            
        return {
            'status' : status,
            'message' : message,
            'result' : result
        }