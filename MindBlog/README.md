# MindBlog
  MindBlog是一个社交的博客项目，允许用户自由发布自己的文章。
  
## 目前版本
### version 0.1
  完成基本的用户操作：注册、登录、登出、修改。  
  完成基本的文章操作：新增、编辑、查看、删除。
  
## 使用方法
### 1. 克隆项目
```
git clone git@github.com:Loounz/MindBlog.git
```
### 2. 命令行或者power shell进入目录/MindBlog/MindBlog下，配置虚拟环境、配置环境参数。
```python
#配置虚拟环境[windows]
$ python -m venv venv
$ .\venv\Scripts\activate
(venv) $ pip install -r requirements.txt

#配置环境参数
(venv)$ $env:FLASK_APP='MindBlog'
(venv)$ $env:FLASK_ENV='development'
(venv)$ flask --debug run
```
### 3. 浏览器输入本地链接即可访问应用。
```
http://127.0.0.1:5000
```
### 4. 使用账号：looun@foxmail.com 密码：123456 可登录账号
### 5. 也可以自己注册账号。
```python
#给自己账号构造一些文章数据
(venv)$ flask fakearticle [你的用户名]
#给整个项目构造一些用户和文章数据
(venv)$ flask fakedata
```

## 预览
live demo

