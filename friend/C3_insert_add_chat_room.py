import pymongo
import json
import html
from pymongo import MongoClient
import pymysql
from datetime import datetime,timedelta
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
env_channel_account = os.getenv("CHANNEL_ACCOUNT")

# # 單聊加入chat_room的時間條件
# env_for_c3_time_start = os.getenv("FORC3ADD_CHAT_ROOM_START")
# env_for_c3_time_end = os.getenv("FORC3ADD_CHAT_ROOM_END")

# ========================sql env
db = pymysql.connect(host=f'{env_url}',
                     user=f'{env_user}',
                     password=f'{env_password}',
                     database=f'{env_database}')


cursor = db.cursor()

time_difference = timedelta(hours=8)

start_time_o = env_start_time
end_time_o = env_end_time
channel_account = env_channel_account

date_format = "%Y-%m-%d %H:%M:%S.%f"
date_format_2 = "%Y-%m-%d"

start = datetime.strptime(env_start_time, date_format_2)
end = datetime.strptime(env_end_time, date_format_2)
print(f"start:{start}")
print(f"end:{end}")


# sql4 = f""" SELECT a.user_id_1, a.user_id_2, a.create_time FROM `chat_friend` as a
#                     where a.create_time >='{start_time}' AND a.create_time <'{end_time}'
#                     order by a.user_id_1 ASC ;"""

sql4 = f""" SELECT a.user_id_1, a.user_id_2, a.create_time FROM `chat_friend` as a
                    where a.create_time >='{start}' AND a.create_time < '{end}'
                    order by a.user_id_1 ASC ;"""


cursor.execute(sql4)
resjoin = cursor.fetchall()
count = len(resjoin)
print(f"count: {count}")

for i in range(0,count):
    room_name = ''
    try:
        room_icon = f"{resjoin[i][0]}|{resjoin[i][1]}"
        print(f"room_icon: {room_icon}")
        room_name = f"{resjoin[i][0]}|{resjoin[i][1]}"
        createTime = f"{resjoin[i][2]}"

        print(f"room_name: {room_name}")

        # 塞chat_room
        sql = f"""INSERT INTO chat_room(room_name,create_time,type,room_icon,content_id,user_count,channel_account,room_mute_type,user_id,share_file_status)
                VALUES ('{room_name}','{createTime}',0,'{room_icon}',1,2,'{channel_account}',0,{resjoin[i][0]},1);"""
        cursor.execute(sql)
        db.commit()


    except Exception as e:
            # 如果发生错误则回滚
            db.rollback()
            print(f"Error: {str(e)}")
   
# # 关闭数据库连接
db.close()
   



