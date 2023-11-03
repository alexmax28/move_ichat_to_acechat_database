# insert chat_record

import pymongo
import json
import html
from pymongo import MongoClient
import pymysql
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os
import re
import datetime
eight_hours = datetime.timedelta(hours=8)
load_dotenv()
# ============== ENV
env_url = os.getenv("DATABASE_URL")
env_user = os.getenv("USER")
env_password = os.getenv("PASSWORD")
env_database = os.getenv("DATABASE")
env_mongodb_url = os.getenv("MONGODB_URL")
env_start_time = os.getenv("START_TIME")
env_end_time = os.getenv("END_TIME")
# 執行開始時間
start_run_time = datetime.datetime.now()

# =========mongo
myclient = pymongo.MongoClient(env_mongodb_url)

# shiku_room
mydb = myclient["tigase"]
mycol = mydb["tig_ma_msgs"]
# 濾時間
time_difference = timedelta(hours=8)

# 今年
# start_date = datetime.datetime(2023, 1, 1, 00, 00, 00, 000)
# end_date = datetime.datetime(2023, 11, 2, 8, 00, 00, 000)
start_date = datetime.datetime(2023, 11, 2)
end_date = datetime.datetime(2023, 11, 3)

# # 每日
# start_date = datetime.datetime(2023, 11, 1, 8, 00, 00, 000)
# end_date = datetime.datetime(2023, 11, 2, 8, 00, 00, 000)


print(end_date)


query = {"ts" : {"$gte":start_date, "$lt" : end_date}}
cur = mycol.find(query).sort([("ts", pymongo.ASCENDING)])
# 總數
mongocount = cur.count()
print(mongocount)

# # ========================sql 232
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


cursor = db.cursor()


# 總數
# mysqlcount = mycol.count()
print(mongocount)

# print(cur)
for n in range(0,mongocount):


    if cur[n]['direction'] == "incoming":
        continue

    content_type_m = cur[n]['body2']['type']

    # if content_type_m == 1:
    #     content_type = 0
    # elif content_type_m == 2:
    #     content_type = 1
    # else:
    #     continue

    if content_type_m == 1:
        content_type = 0
        objectId_messageId = ''
    elif content_type_m == 94:
        content_type = 2
        objectId = f"{cur[n]['body2']['objectId']}"
        data = json.loads(objectId)
        objectId_messageId = data['messageId']
        print(f'objectId_messageId: {objectId_messageId}')
    else:
        continue
    

    if 'toUserId' not in  cur[n]['body2']:
        continue

    if 'content' not in  cur[n]['body2']:
        continue

    if cur[n]['body2']['toUserId'] is None:
        continue



    body2_content = cur[n]['body2']['content']
    # create_time = cur[n]['ts'] + timedelta(hours=8)
    create_time = cur[n]['ts']
    fromUserId = cur[n]['body2']['fromUserId']
    toUserId = cur[n]['body2']['toUserId']

    # 去除跳脫字元的內容
    pattern = r'.*\\.*'
    pattern_2 = r"\'"
    match = re.search(pattern,body2_content)
    match_2 = re.search(pattern_2,body2_content)
    if match or match_2:
        print("*字符串包含转义字符:")
        continue



    if int(fromUserId) < int(toUserId):
        room_id_m = f"{fromUserId}|{toUserId}"
    else:
        room_id_m = f"{toUserId}|{fromUserId}"

    room_id = ''
    room_name = ''
    account_type = 0
    user_id = cur[n]['body2']['fromUserId']
    # user_name = str(cur[n]['body2']['fromUserName'])
    nick_name = ''
    room_type = 0
    

    channel_account = 'None'
    uuId = 'None'
    

    print("===================================")


    sql1 = f'''select room_id, room_name, create_time from chat_room
            where room_icon = '{room_id_m}';'''
    
    sql2 = f'''select user_id, user_name, create_time, nick_name from chat_user
            where user_id = {int(user_id)};'''
    

    try:
        cursor.execute(sql1)
        ressql1 = cursor.fetchone()

        if ressql1 is None:
            continue
        room_id = ressql1[0]
        room_name = ressql1[1]

        
        print(f"content_type_m: {content_type_m}")
        print(f"room_id_m: {room_id_m}")

        print(f"body2_content: {body2_content}")
        print(f"create_time: {create_time}")
        print(f"room_id: {room_id}")
        print(f"room_name: {room_name}")

        cursor.execute(sql2)
        ressql2 = cursor.fetchone()

        user_name = str(ressql2[1])
        nick_name = ressql2[3]
        print(f"nick_name: {nick_name}")

        sql3 = f"""INSERT INTO chat_record(chat_content, create_time, room_id, room_name, account_type, user_id, user_name, nick_name, room_type, content_type, channel_account, uuId)
                                 VALUES ('{body2_content}','{create_time}',{room_id},'{room_name}',{account_type},{user_id},'{user_name}','{nick_name}',{room_type},{content_type},'{channel_account}','{uuId}');"""
        print(sql3)
        
        cursor.execute(sql3)
        db.commit()

    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()
        print(f"Error: {str(e)}")

        break

    
   
# 关闭数据库连接
db.close()
# 結束執行時間
end_run_time = datetime.datetime.now()

print(f"開始執行時間: {start_run_time}")
print(f"結束執行時間: {end_run_time}")