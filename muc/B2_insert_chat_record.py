
# muc_storage_1 > chat_record_2
import pymongo
import json
import html
from pymongo import MongoClient
import pymysql
from datetime import datetime
import re
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

# =========mongo
# myclient = pymongo.MongoClient(env_mongodb_url)

# muc_history
# mydb = myclient["tigase"]
# mycol = mydb["muc_history"]
# muc_history_cur = mycol.find()

# # shiku_room_member
# mycol2 = mydb["shiku_room_member"]
# shiku_room_member = mycol2.find()
# 總數
# count = muc_history_cur.count()

# # # =========sql 232
# db = pymysql.connect(host='192.168.100.232',
#                      user='root',

#                      password='XhR7r5yPBlmImHAD',
#                      database='iChat')
# # =========sql 210
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


# # b.room_id 改 b.id
# sql3 = f"""SELECT a.chat_content, a.create_time, IFNULL(b.id,0), IFNULL(d.room_name,"null"), a.account_type, a.user_id, c.user_name, c.nick_name, a.room_type, a.content_type, a.channel_account, a.uuId, a.body2_messageId, a.objectId_messageId
#             FROM `muc_storage` as a
#             left join im_mapping as b
#             on a.room_id = b.im_jid
#             left join chat_user as c
#             on a.user_id = c.user_id
#             left join chat_room as d
#             on b.id = d.room_id
# 			where a.content_type in (0,1,7,8,3,4,6,2) and a.create_time >='{env_start_time}' AND a.create_time <'{env_end_time}';"""


sql3 = f"""SELECT a.chat_content, a.create_time, IFNULL(d.room_id,0), IFNULL(d.room_name,"null"), a.account_type, a.user_id, c.user_name, c.nick_name, a.room_type, a.content_type, a.channel_account, a.uuId, a.body2_messageId, a.objectId_messageId
            FROM `muc_storage` as a
            left join im_mapping as b
            on a.room_id = b.im_jid
            left join chat_user as c
            on a.user_id = c.user_id
            left join chat_room as d
            on b.im_jid = d.jid
			where a.content_type in (0,1,7,8,3,4,6,2) and a.create_time >='{env_start_time}' AND a.create_time <'{env_end_time}';"""

sqlcursor.execute(sql3)
resjoin = sqlcursor.fetchall()
# print(resjoin)
count = len(resjoin)
print(len(resjoin))


for i in range(0,count):
    try:
        #  # test
        sql4 = f"""INSERT INTO chat_record(chat_content, create_time, room_id, room_name, account_type ,user_id, user_name, nick_name, room_type, content_type, channel_account, uuId, body2_messageId, objectId_messageId)
                        VALUES ('{resjoin[i][0]}',DATE_ADD('{resjoin[i][1]}', INTERVAL 8 HOUR),{int(resjoin[i][2])},'{resjoin[i][3]}',{int(resjoin[i][4])},{int(resjoin[i][5])},'{resjoin[i][6]}','{resjoin[i][7]}',{resjoin[i][8]},{resjoin[i][9]},'{resjoin[i][10]}','{resjoin[i][11]}','{resjoin[i][12]}','{resjoin[i][13]}')"""
        print(sql4)
        sqlcursor.execute(sql4)
        db.commit()

    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()
        print(f"Error: {str(e)}")
   
# 关闭数据库连接
db.close()


