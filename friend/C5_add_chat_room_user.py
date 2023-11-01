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

# =========mongo
# myclient = pymongo.MongoClient("mongodb://192.168.100.241:28018/")

# # shiku_room
# mydb = myclient["imRoom"]
# mycol = mydb["shiku_room"]
# cur = mycol.find()

# # shiku_room_member
# mycol2 = mydb["shiku_room_member"]
# shiku_room_member = mycol2.find()

# count = shiku_room_member.count()


# ========================sql 232
# db = pymysql.connect(host='192.168.100.232',
#                      user='root',

#                      password='XhR7r5yPBlmImHAD',
#                      database='iChat')

# # ========================sql 210
# db = pymysql.connect(host='192.168.100.210',
#                      user='root',

#                      password='12345678',
#                      database='alexjdbc')

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
# start_time = datetime.strptime(start_time_o, date_format) - time_difference
# end_time = datetime.strptime(end_time_o, date_format) - time_difference

start_time = datetime.strptime(start_time_o, date_format)
end_time = datetime.strptime(end_time_o, date_format)

sql = f""" SELECT a.room_id, a.room_icon, a.create_time FROM `chat_room` as a
            where a.type = 0 and a.create_time >='{start_time}' AND create_time <'{end_time}';"""

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