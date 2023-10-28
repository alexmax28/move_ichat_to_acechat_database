
# update chat_record (chat_content)
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

# # =========sql 232
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


cursor = db.cursor()
sql =  f'''select id,chat_content,create_time,room_id,room_name,account_type,user_id,user_name,nick_name,room_type,content_type,channel_account,uuId,body2_messageId,objectId_messageId
 from chat_record 
 where create_time >='{env_start_time}' AND create_time <'{env_end_time}';
 '''
cursor.execute(sql)
res = cursor.fetchall()
count = len(res)
print(count)




for i in range(0,count):
    # print(res[i])
    if res[i][10] == 2:
        
        objid = res[i][14]
        sql2 =  f'''select id,chat_content,create_time,room_id,room_name,account_type,user_id,user_name,nick_name,room_type,content_type,channel_account,uuId,body2_messageId,objectId_messageId
            from chat_record
             where body2_messageId = '{objid}' and create_time >='{env_start_time}' AND create_time <'{env_end_time}';
             '''
        cursor.execute(sql2)
        res2 = cursor.fetchone()
        chat_record_id = ''
        chat_content = ''
        o_content = ''
        record_id = int(res[i][0])
        
        if res2 is None:
            chat_record_id = 'none'
            chat_content = res[i][1]
            o_content = 'none'
        elif res2 is not None:
            chat_record_id = res2[0]
            chat_content = res[i][1]
            o_content = res2[1]
            

        print(f"============================================")
        print(f"objid: {res[i][14]}")
        print(f"chat_record_id: {chat_record_id}")
        print(f"o_content: {o_content}")
        print(f"chat_content: {chat_content}")
        
        chat_record_chat_content = f"{chat_record_id}||{o_content}||{chat_content}"
        print(chat_record_chat_content)
        # print(f"res[i][0]: {res[i][0]}")
        # print(f"res[i][0]type: {type(res[i][0])}")
        

        try:
            sql3 = f"update chat_record set chat_content = '{chat_record_chat_content}' where id = {record_id} and create_time >='{env_start_time}' AND create_time <'{env_end_time}';"
            cursor.execute(sql3)         
            db.commit()
            print(sql3)

        except Exception as e:
            # 如果发生错误则回滚
            db.rollback()
            print(f"Error: {str(e)}")

# 关闭数据库连接

db.close()