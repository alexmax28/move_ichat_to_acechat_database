import pymongo
import json
import html
from pymongo import MongoClient
import pymysql
# from datetime import datetime
import datetime
from dotenv import load_dotenv
import os
load_dotenv()
# ============== ENV
# env_url = os.getenv("DATABASE_URL")
# env_user = os.getenv("USER")
# env_password = os.getenv("PASSWORD")
# env_database = os.getenv("DATABASE")


# ========================mysql env
db = pymysql.connect(host=f'192.168.100.232',
                     user=f'root',
                     password=f'XhR7r5yPBlmImHAD',
                     database=f'iChat')
cursor = db.cursor()
create_time = '2022-05-26 17:05:19'

for i in range(1,2001): 
    inputdb = f"'test{i}','$2a$10$qOePzMxvG311Y9vSm3.Umuxt7xad53.xtqMK0cwcMuQwumSo7C/U.','test{i}','{create_time}',0,1,1,'{15111111111+i}',3,'acechat','000',0,'FRONT_REFRESH_3|{i}'"
    print(inputdb)
# 新增測試表 chat_user
    sql = f"""INSERT INTO chat_user(user_name,password,nick_name,create_time,is_online,type,status,phone,device,channel_account,area_code,data_type,refresh_tId)
            VALUES ({inputdb})"""
    print(sql)

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        print("error")    
        db.rollback()
# 关闭数据库连接
db.close()