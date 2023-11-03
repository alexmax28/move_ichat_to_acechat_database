# add chat_room_user
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
env_start_time = os.getenv("START_TIME")
env_end_time = os.getenv("END_TIME")

# # 單聊加入chat_room的時間條件
# env_for_c3_time_start = os.getenv("FORC3ADD_CHAT_ROOM_START")
# env_for_c3_time_end = os.getenv("FORC3ADD_CHAT_ROOM_END")

# ========================sql env
db = pymysql.connect(host=f'{env_url}',
                     user=f'{env_user}',
                     password=f'{env_password}',
                     database=f'{env_database}')


sqlcursor = db.cursor()


time_difference = timedelta(hours=8)

start_time_o = env_start_time
end_time_o = env_end_time

date_format = "%Y-%m-%d %H:%M:%S.%f"
date_format_2 = "%Y-%m-%d"

start = datetime.strptime(env_start_time, date_format_2)
end = datetime.strptime(env_end_time, date_format_2)

# sql = f""" SELECT a.room_id, a.room_icon, a.create_time FROM `chat_room` as a
#             where a.type = 0 and a.create_time >='{start_time}' AND create_time <'{end_time}';"""

sql = f""" SELECT a.room_id, a.room_icon, a.create_time FROM `chat_room` as a
            where a.type = 0 and a.create_time >='{start}' AND a.create_time < '{end}';"""

sqlcursor.execute(sql)
res = sqlcursor.fetchall()
count = len(res)
print(count)




for i in range(0,count):
   
    try:
        # 执行sql语句
       
        room_id = res[i][0]
        print(f"user_id: {room_id}")
        room_icon = res[i][1]
        print(f"room_icon: {room_icon}")
        create_time= res[i][2]
        print(f"create_time: {create_time}")

        splitted_list = room_icon.split("|")

        if len(splitted_list) == 2:
            first_user_id = splitted_list[0]
            second_user_id = splitted_list[1]

            print("前半部分：", first_user_id)
            print("後半部分：", second_user_id)
        else:
            print("輸入的字串格式不正確，無法拆分成前後兩部分。")

        # sql1 = f""" SELECT a.user_id, a.user_name FROM `chat_user` as a
        #             where a.user_id = {first_user_id};"""
        # sqlcursor.execute(sql1)
        # res1 = sqlcursor.fetchone()
        # inviter = res1[0]


        slq2 = f''' INSERT INTO chat_room_user(user_id,room_id,create_time,leave_time,inviter,inviter_type,mute_type,notification_flag)
                        VALUES ({first_user_id},{room_id},'{create_time}','{create_time}','{first_user_id}',0,0,0);'''
        print(slq2)
        sqlcursor.execute(slq2)
        db.commit()
        

        slq3 = f''' INSERT INTO chat_room_user(user_id,room_id,create_time,leave_time,inviter,inviter_type,mute_type,notification_flag)
                        VALUES ({second_user_id},{room_id},'{create_time}','{create_time}','{first_user_id}',0,0,0);'''
        print(slq3)
        sqlcursor.execute(slq3)
        db.commit()
        


    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()
        print(f"Error: {str(e)}")
   
# 关闭数据库连接
db.close()