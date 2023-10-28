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

# myclient = pymongo.MongoClient(env_mongodb_url)

# mydb = myclient["imapi"]
# mycol = mydb["u_friends"]
# cur = mycol.find()

# count = cur.count()
# print(count)

# # # ========================sql 232
# db = pymysql.connect(host='192.168.100.232',
#                      user='root',

#                      password='XhR7r5yPBlmImHAD',
#                      database='iChat')

# # # ========================sql 210
# db = pymysql.connect(host='192.168.100.210',
#                      user='root',

#                      password='12345678',
#                      database='alexjdbc')

# ========================sql env
db = pymysql.connect(host=f'{env_url}',
                     user=f'{env_user}',
                     password=f'{env_password}',
                     database=f'{env_database}')


cursor = db.cursor()

time_difference = timedelta(hours=8)

start_time_o = env_start_time
end_time_o = env_end_time

date_format = "%Y-%m-%d %H:%M:%S.%f"
# start_time = datetime.strptime(start_time_o, date_format) - time_difference
# end_time = datetime.strptime(end_time_o, date_format) - time_difference

start_time = datetime.strptime(start_time_o, date_format)
end_time = datetime.strptime(end_time_o, date_format)


sql4 = f""" SELECT a.user_id_1, a.user_id_2, a.create_time FROM `chat_friend` as a
                    where a.create_time >='{start_time}' AND a.create_time <'{end_time}'
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


        # sql5 = f''' select user_id, nick_name from chat_user
        #     where user_id = {resjoin[i][0]}'''
        # cursor.execute(sql5)
        # ressql5 = cursor.fetchone()
        # # print(ressql5[1])

        # sql6 = f''' select user_id, nick_name from chat_user
        #     where user_id = {resjoin[i][1]}'''
        # cursor.execute(sql6)
        # ressql6 = cursor.fetchone()
        # # print(ressql6[1])

        # room_name = f"{ressql5[1]}|{ressql6[1]}"

        room_name = f"{resjoin[i][0]}|{resjoin[i][1]}"
        createTime = f"{resjoin[i][2]}"

        print(f"room_name: {room_name}")

        # 塞chat_room
        sql = f"""INSERT INTO chat_room(room_name,create_time,type,room_icon,content_id,user_count,channel_account,room_mute_type,user_id)
                VALUES ('{room_name}','{createTime}',0,'{room_icon}',1,2,'zlcai',0,{resjoin[i][0]});"""
        cursor.execute(sql)
        db.commit()

    except Exception as e:
            # 如果发生错误则回滚
            db.rollback()
            print(f"Error: {str(e)}")
   
# # 关闭数据库连接
db.close()
   



