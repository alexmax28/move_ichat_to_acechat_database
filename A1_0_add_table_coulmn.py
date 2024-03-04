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
    sql7 = f"""ALTER TABLE chat_room ADD im_room_id varchar(100) DEFAULT NULL;
        """   
    print(sql7)
    sqlcursor.execute(sql7)
    db.commit()

    sql8 = f"""ALTER TABLE chat_room ADD jid varchar(100) DEFAULT NULL;
        """
    print(sql8)
    sqlcursor.execute(sql8)
    db.commit()

    sql9 = f"""ALTER TABLE chat_record ADD body2_messageId varchar(255) DEFAULT NULL;
        """
    print(sql9)
    sqlcursor.execute(sql9)
    db.commit()

    sql10 = f"""ALTER TABLE chat_record ADD objectId_messageId varchar(255) DEFAULT NULL;
        """
    print(sql10)
    sqlcursor.execute(sql10)
    db.commit()

except Exception as e:
    # 如果发生错误则回滚
    db.rollback()
    print(f"Error: {str(e)}")
   
# 更新邀請者欄位

# 关闭数据库连接
db.close()