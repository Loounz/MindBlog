'''

'''

from flask.views import MethodView
from MindBlog.models import Comment

# 初始化Api
def commentApiInit(app):
    comment_view = CommentApi.as_view('comment_api');
    app.add_url_rule('/comments/',defaults = {'comment_id' : None}, view_func = comment_view, methods = ['GET',]);
    app.add_url_rule('/comments/<int:comment_id>',view_func = comment_view, methods = ['GEt','PUT','DELETE']);
    app.add_url_rule('/comments/',view_func = comment_view, methods = ['POST']);
    
# 评论Api
class CommnetApi(MethodView):
    def get(self, comment_id):
        pass;
    
    def post(self):
        pass;