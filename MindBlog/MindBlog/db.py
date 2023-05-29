from flask_sqlalchemy import SQLAlchemy

g_db = SQLAlchemy();

# 初始化数据库【不太完善，每次启动都会初始化一次】
def dbInit(app):
    print('init database');
    g_db.init_app(app);
    #g_db.drop_all();
    g_db.create_all();

# 写入数据
def dbAddData(data):
    try:
        g_db.session.add(data);
        g_db.session.commit();
        return True;
    except Exception as error:
        # [todo: 把错误日志写进文本]
        print('dbAddData error[code: %s] file: %s' %(error,__file__));
        return False;

# 更新函数
def dbUpdateData(data):
    try:
        data.verified = True;
        g_db.session.commit();
        return True;
    except Exception as error:
        # [todo: 把错误日志写进文本]
        print('dbUpdateData error[code: %s] file: %s' %(error,__file__));
        return False;
    
# 删除数据
def dbDeleteData(data):
    try:
        g_db.session.delete(data);
        g_db.session.commit();
        return True;
    except Exception as error:
        # [todo: 把错误日志写进文本]
        print('dbDeleteData error[code: %s] file: %s' %(error,__file__));
        return False;

# 查询 表单 所有数据
def dbQueryAll(tableObj):
    return tableObj.query.all();
    
# 查询表单里的特定数据，返回数据。
def dbQueryOne(tableObj, data):
    return tableObj.query.get(data);