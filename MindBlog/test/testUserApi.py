from ..MindBlog.api.UserApi import generateToken,checkToken

if __name__ == '__main__':
    data = {
        "UserName":"looun",
        "UserId":123456,
        "UserPassword":"looun.com"
    }
    
    token = generateToken(data);
    print(token);
    
    data2 = checkToken(token);
    print(data2);