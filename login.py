from flask import Flask
app = Flask(__name__)
from flask import render_template
from flask import request
import traceback
import pymysql
import re

app = Flask(__name__,
static_folder = "/home/doubanMovie/static",
template_folder = "/home/doubanMovie/src")

#电影列表，与数据库对应
movieDict={"爱情": 1, "喜剧": 2, "动画": 3, "剧情": 4, "恐怖": 5, "惊悚": 6, "科幻": 7, "动作": 8,
           "悬疑": 9, "犯罪": 10, "冒险": 11, "战争": 12, "奇幻": 13, "运动": 14, "家庭": 15,
           "古装": 16, "武侠": 17, "西部": 18, "历史": 19, "传记": 20, "歌舞": 21, "黑色电影": 22,
           "短片": 23, "纪录片": 24, "其他": 25}

# @app.route('/',methods=['GET','POST'])
# def login():
#     print("login被调用")
#     print(request)
#     return "成功"


# @app.route('/regist',methods=['POST'])
# def registuer():
#     print('你好')
#     return"成功"

def checkPsd(psd):
    str="[^a-zA-Z0-9]"
    list=re.search(str, psd, flags=0)
    if psd=='' or list != None:
        return False
    else:
        return True

#获取注册请求及处理
@app.route('/registuser',methods=['POST'])
def getRegistRequest():
    print(request)
    print("注册方法被调用")
    print(request)
    parameters = request.form
    # print(parameters)
    username=parameters.get('user')
    psd=parameters.get('password')
    conpsd=parameters.get('conpsd')
    likes=parameters.getlist('movietype')
    # print(movieDict[likes[0]])
#把用户名和密码注册到数据库中
    if username=='':
        return '用户名不能为空'
    if psd!=conpsd:
        return '两次输入密码不符'
    if psd=='':
        return '密码不能为空'
    if not checkPsd(psd):
        return '密码不符合规则'
    #连接数据库,此前在数据库中创建数据库TESTDB
    # db = pymysql.connect("127.0.0.1","root","root","user" )
    db = pymysql.connect(host='62.234.52.40',port=3306,user='douban',
                         password='123456',db='douban')
    cursor = db.cursor()
    # 查重复用户名
    sql = "select * from user where user=" + "'" + username + "'"
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(len(results))
        if len(results) == 0:
            pass
        else:
            return '用户名重复'
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()

    # SQL 新增用户
    sql = "INSERT INTO user(user, password) VALUES ("+"'"+username+"'"+", "+"'"+psd+"'"+")"
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        #抛出错误信息
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        return '0'
    sql = "select id from user where user=" + "'" + username + "'"
    cursor.execute(sql)
    userid = cursor.fetchall()
    # 提交到数据库执行
    db.commit()
    for like in likes:
        cursor.execute('INSERT INTO userlike(userid, movieid) VALUES ( %s,%s)', (userid[0][0], movieDict[like]))
        # 提交到数据库执行
        db.commit()

    db.close()
    return "1"



#获取登录参数及处理
@app.route('/login',methods=['GET','POST'])
def getLoginRequest():
    print("登录方法被调用")
    # return "登录方法被调用"
    # db = pymysql.connect("localhost","root","root","user" )
    db = pymysql.connect(host='62.234.52.40', port=3306, user='douban', password='123456', db='douban')
    cursor = db.cursor()
    sql = "select * from user where user="+"'"+request.args.get('user')+\
          "'"+" and password="+"'"+request.args.get('password')+"'"+""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print(len(results))
        if len(results)==1:
            return '1'
        else:
            return '0'
        db.commit()
    except:
        traceback.print_exc()
        db.rollback()
    db.close()

if __name__ == '__main__':
    # app.run(debug=True,port=5000)
    app.run(host='0.0.0.0',port=5000)