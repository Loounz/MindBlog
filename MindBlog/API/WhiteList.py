
'''
api白名单列表
仅让在白名单内的ip访问后端接口。
'''
from flask import request;

g_whiteList = ['127.0.0.1'];

# 是否白名单
def wlisWhiteList():
    remote = request.remote_addr;
    if remote in g_whiteList:
        return True;
    
    return False;