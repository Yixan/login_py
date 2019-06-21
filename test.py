from flask import Flask
app = Flask(__name__)
from flask import render_template
from flask import request
import traceback
import pymysql
import re
from flask_cors import CORS
import os
import ConKafka
app = Flask(__name__)

CORS(app)

#电影列表，与数据库对应
movieDict={'爱情': 1, '喜剧': 2, '动画': 3, '剧情': 4, '恐怖': 5, '惊悚': 6, '科幻': 7, '动作': 8,
           '悬疑': 9, '犯罪': 10, '冒险': 11, '战争': 12, '奇幻': 13, '运动': 14, '家庭': 15,
           '古装': 16, '武侠': 17, '西部': 18, '历史': 19, '传记': 20, '歌舞': 21, '黑色电影': 22,
           '短片': 23, '纪录片': 24, '其他': 25}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/regist')
def registuer():
    return render_template('registuser.html')

# #设置响应头
# def Response_headers(content):
#     resp = Response(content)
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp
# 验证密码是否合法

# def dbCon():


def checkPsd(psd):
    str="[^a-zA-Z0-9]"
    list=re.search(str, psd, flags=0)
    if psd=='' or list != None:
        return False
    else:
        return True

#获取注册请求及处理
@app.route('/registuser',methods=['GET','POST'])
def getRegistRequest():
    print(request)
    parameters = request.args
    print(parameters)
    username=parameters.get('user')
    psd=parameters.get('password')
    conpsd=parameters.get('conpsd')
    likes=parameters.getlist('movietype').split(',')
    print(movieDict[likes[0]])
    while request.args.get('movietype')!=None:
        likes.append(request.args.get('movietype'))
    print(likes)
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
    db = pymysql.connect(host='114.116.15.154',port=3306,user='sspku',password='sspku06',db='movie')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 查重复用户名
    sql = "select * from user where user=" + "'" + username + "'"
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        print(len(results))
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
        return '注册失败'
    sql = "select id from user where user=" + "'" + username + "'"
    cursor.execute(sql)
    userid = cursor.fetchall()
    print(userid)
    # 提交到数据库执行
    db.commit()
    if len(likes)==0:
        return "请选择偏好"
    for like in likes:
        cursor.execute('INSERT INTO userlike(userid, movieid) VALUES ( %s,%s)',
                       (userid[0][0], movieDict[like]))
        db.commit()


    # 关闭数据库连接
    db.close()
    # 注册成功之后跳转到登录页面
    return "1"
#获取登录参数及处理
@app.route('/login',methods=['GET','POST'])
def getLoginRequest():
#查询用户名及密码是否匹配及存在
    #连接数据库,此前在数据库中创建数据库TESTDB
    # db = pymysql.connect("localhost","root","root","user" )
    db = pymysql.connect(host='114.116.15.154', port=3306, user='sspku',
                         password='sspku06', db='movie')
# 要不我给你一个密码是字母的账号
# 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    user=str(request.args.get('user'))
    psd=str(request.args.get('password'))
    print("user:%s psd:%s"%(user,psd))
    sql = "select * from user where user=" + "'" + user + \
      "'" + " and password=" + "'" + psd + "'"
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        print(len(results))
        if len(results)==1:
            return '1'
        else:
            return '0'
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
    # 关闭数据库连接
    db.close()

@app.route('/prefer',methods=['GET','POST'])
def prefer():
    movieid=request.args.get('movieid')
    username=request.args.get('username')
    prefer=request.args.get('like')
    ConKafka.connect(username+","+movieid+","+prefer)
    print("结束")

    return "1"




if __name__ == '__main__':
    app.run(debug=True,port=8080)
    #  app.run(host='0.0.0.0',port=8080)