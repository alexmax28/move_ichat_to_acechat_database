import pymongo
import json
import html
from pymongo import MongoClient
import pymysql
myclient = pymongo.MongoClient("mongodb://192.168.100.210:29300/")

mydb = myclient["imapi"]
mycol = mydb["user"]
# collst = mydb.list_collection_names()


# dblist = myclient.list_database_names()
# if "imRoom" in dblist:
#     print("数据库已存在！")


cur = mycol.find()

# print(type(cur))
inputdb = f"{cur[0]['_id']},{cur[0]['phone']},{cur[0]['password']},{cur[0]['nickname']},{cur[0]['telephone']}"
print(inputdb)
# print(f"{cur[0]['_id']},{cur[0]['phone']},{cur[0]['password']},{cur[0]['nickname']},{cur[0]['createTime']},{cur[0]['phone']},")


# for ccc in cur:
#     # nickname = str(ccc['nickname'])
#     # uid = str(ccc['_id'])
#     # print(f"nickname:{nickname}")
#     print(ccc)


db = pymysql.connect(host='192.168.100.210',
                     user='root',
                     password='12345678',
                     database='alexjdbc')
cursor = db.cursor()

sql = f"""INSERT INTO chat_user(user_id,user_name,password,nickname,phone)
         VALUES ({inputdb})"""

try:
   # 执行sql语句
   cursor.execute(sql)
   # 提交到数据库执行
   db.commit()
except:
   # 如果发生错误则回滚
   db.rollback()
 
# 关闭数据库连接
db.close()