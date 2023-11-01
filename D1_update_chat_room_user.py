# room_user_test_3 chat_room_user_4
import pymongo
import json
import html
from pymongo import MongoClient
import pymysql
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()
# ============== ENV
env_url = os.getenv("DATABASE_URL")
env_user = os.getenv("USER")
env_password = os.getenv("PASSWORD")
env_database = os.getenv("DATABASE")
env_mongodb_url = os.getenv("MONGODB_URL")
env_start_time = os.getenv("START_TIME")
env_end_time = os.getenv("END_TIME")

# ========================sql env
db = pymysql.connect(host=f'{env_url}',
                     user=f'{env_user}',
                     password=f'{env_password}',
                     database=f'{env_database}')


sqlcursor = db.cursor()

   
try:
    # 执行sql语句
    #  # test
    sql3 = f"""
        update chat_room_user
		set room_user_type = 1
		where user_id = inviter"""
    
    print(sql3)
    sqlcursor.execute(sql3)
    db.commit()

except Exception as e:
    # 如果发生错误则回滚
    db.rollback()
    print(f"Error: {str(e)}")
   
# 更新邀請者欄位

# 关闭数据库连接
db.close()