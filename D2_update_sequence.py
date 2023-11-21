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
    sql4 = f"""
        SELECT count(id) FROM chat_record"""
    
    print(sql4)
    sqlcursor.execute(sql4)
    db.commit()

    resjoin = sqlcursor.fetchone()
    chat_record_total = resjoin[0]
    print(chat_record_total)
    try:
        sql5 = f"""
        UPDATE sequence 
        SET current_value = {int(chat_record_total)}
        """
        
        sqlcursor.execute(sql5)
        db.commit()
        print(sql5)

    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()
        print(f"Error: {str(e)}")


except Exception as e:
    # 如果发生错误则回滚
    db.rollback()
    print(f"Error: {str(e)}")
   
# 更新邀請者欄位

# 关闭数据库连接
db.close()