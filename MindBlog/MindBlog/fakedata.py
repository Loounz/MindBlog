from faker import Faker
from MindBlog.models import User,Article
from MindBlog.db import dbAddData,dbUpdateData,dbDeleteData,g_db
from sqlalchemy.exc import IntegrityError
from random import randint

fake = Faker();

# 初始化number数量的用户信息
def fakeUsers(number):
    for i in range(int(number)):
        user = User(UserId=User.newUserId(),
                 UserName = fake.user_name(),
                 UserPassword = 'password',
                 UserEmail = fake.email());
        try:
            dbAddData(user);
        except IntegrityError:
            g_db.session.rollback();

# 初始化给每个用户生成1~number数量的文章信息
def fakeArticles(number):
    users:User = User.query.all();
    
    for user in users:
        num = randint(1,number);
        for index in range(num):
            post = Article(ArticleId = Article.newPostId(),
                           ArticleTitle = fake.name(),
                           ArticleContent = fake.text(),
                           ArticlePostDate = fake.past_date(),
                           ArticleRead = randint(1,10000),
                           ArticleAuthor = user);
            try:
                dbAddData(post);
            except IntegrityError:
                g_db.session.rollback();

# 初始化给每个用户生成1~number数量的文章信息
def fakeArticlesforUser(user):
    user:User = User.query.filter_by(UserName=user).first();
    if(not user):
        print('user %s not exist.' %user);
        return False;
    number = 20;
    num = randint(1,number);
    for index in range(num):
        post = Article(ArticleId = Article.newPostId(),
                           ArticleTitle = fake.name(),
                           ArticleContent = fake.text(),
                           ArticlePostDate = fake.past_date(),
                           ArticleRead = randint(1,10000),
                           ArticleAuthor = user);
        try:
            dbAddData(post);
        except IntegrityError:
            g_db.session.rollback();
    
