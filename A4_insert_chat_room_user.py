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
# b.room_id
# sql4 = f"""select a.id, a.user_id ,b.id, a.create_time, a.leave_time, d.user_name
#             from room_user_test as a
#             left join im_mapping as b
#             on a.room_id = b.im_room_id
#             LEFT JOIN chat_room as c
#             on b.id = c.room_id
#             LEFT JOIN chat_user as d
#             on c.user_id = d.user_id
#             where a.create_time >='{env_start_time}' AND a.create_time <'{env_end_time}'
#             order by a.id;"""

sql4 = f"""
SELECT
	a.id,
	a.user_id,
	c.room_id,
	a.create_time,
	a.leave_time,
	c.user_id 
FROM
	room_user_test AS a
    LEFT JOIN chat_room AS c ON a.room_id = c.im_room_id
    where a.create_time >='{env_start_time}' AND a.create_time <'{env_end_time}'
    order by a.id;"""

sqlcursor.execute(sql4)
resjoin = sqlcursor.fetchall()
print(len(resjoin))

for i in range(0,len(resjoin)):
   
    try:
        # 执行sql语句
        #  # test
        sql3 = f"""INSERT INTO chat_room_user(user_id,room_id,create_time,leave_time,inviter,inviter_type,mute_type,notification_flag,clean_time,update_time)
                        VALUES ({resjoin[i][1]},'{resjoin[i][2]}','{resjoin[i][3]}','{resjoin[i][4]}','{resjoin[i][5]}',0,0,0,'{resjoin[i][3]}','{resjoin[i][3]}')"""
        
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