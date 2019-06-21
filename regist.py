import pymysql

db = pymysql.connect(host='62.234.52.40', port=3306, user='douban',
                     password='123456', db='douban')
cursor = db.cursor()
cursor.execute('INSERT INTO userlike (userid, movieid) VALUES ( "1","1")')
# cursor.execute(sql)
# 提交到数据库执行
db.commit()
# /components/login