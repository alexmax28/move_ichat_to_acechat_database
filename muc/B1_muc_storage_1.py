
# muc_history insert muc_storage_1
import pymongo
import json
import html
from pymongo import MongoClient
import pymysql
from datetime import datetime,timedelta
import re
import json
from dotenv import load_dotenv
import os
import datetime
eight_hours = datetime.timedelta(hours=8)
load_dotenv()
# ============== ENV
env_url = os.getenv("DATABASE_URL")
env_user = os.getenv("USER")
env_password = os.getenv("PASSWORD")
env_database = os.getenv("DATABASE")
env_mongodb_url = os.getenv("MONGODB_URL")
env_start_time = os.getenv("MUC_START_TIME")
env_end_time = os.getenv("MUC_END_TIME")
env_channel_account = os.getenv("CHANNEL_ACCOUNT")

# =========mongo
myclient = pymongo.MongoClient(env_mongodb_url)

# muc_history
mydb = myclient["tigase"]
mycol = mydb["muc_history"]

# 濾時間
#大於等於start_time 小於end_time
time_difference = timedelta(hours=8)

# # 今年
# start_date = datetime.datetime(2023, 1, 1).timestamp()
# end_date = datetime.datetime(2023, 11, 17).timestamp()


# # 每日
# 11/5 create_time 改成 body2.timeSend
# start_date = datetime.datetime(2023, 11, 18).timestamp()
# end_date = datetime.datetime(2023, 11, 19).timestamp()
start_date = datetime.datetime(2023, 11, 26)
end_date = datetime.datetime(2023, 11, 27)

# # # # 修改少的
# start_date = datetime.datetime(2023, 11, 17,7,56,00).timestamp()
# end_date = datetime.datetime(2023, 11, 17,7,58,00).timestamp()


# # 11/5 create_time 改成 body2.timeSend
# query = {"body2.timeSend" : {"$gte":start_date,"$lt":end_date}}
# cur = mycol.find(query).sort([("body2.timeSend", pymongo.ASCENDING)])

# 11/18 create_time 改成 timestamp
query = {"timestamp" : {"$gte":start_date,"$lt":end_date}}
cur = mycol.find(query).sort([("timestamp", pymongo.ASCENDING)])

# 總數
mongocount = cur.count()
print(mongocount)


# ========================sql env
db = pymysql.connect(host=f'{env_url}',
                     user=f'{env_user}',
                     password=f'{env_password}',
                     database=f'{env_database}')


sqlcursor = db.cursor()

# print(muc_history_cur[0]["_id"])

for i in range(0,mongocount):
    pattern = r"@(\S+)"
    
    if "content" not in cur[i]['body2']:
        continue
    
    if cur[i]['body2']['content']:
        body2_content = cur[i]['body2']['content']
    else:
        body2_content = ''
# # 10/29原始日期設定
#     create_time_ts = cur[i]['timestamp']
#     # create_time = create_time_ts + timedelta(hours=8)
#     create_time = create_time_ts
#     print(create_time)

# # 11/5 create_time 改成 body2.timeSend
#     timeSend = cur[i]['body2']['timeSend']
#     create_time = datetime.datetime.fromtimestamp(timeSend)

# 11/7 create_time 改抓 timestamp
    create_time = cur[i]['timestamp']

    room_jido = cur[i]['room_jid']
    room_jid = re.sub(pattern, "", room_jido) #room_id
    room_name = room_jid
    account_type = 0
    user_id = cur[i]['body2']['fromUserId']
    user_name = user_id
    nick_name = user_id
    room_type = 1
    channel_account = env_channel_account
    uuId = 'null'
    body2_messageId = cur[i]['body2']['messageId']
    print(f'body2_messageId: {body2_messageId}')
    # content_type = muc_history_cur[i]['body2']['type']

    if cur[i]['body2']['type'] == 1:
        content_type = 0
        objectId_messageId = ''
    elif cur[i]['body2']['type'] == 2:
        content_type = 1
        objectId_messageId = ''
    elif cur[i]['body2']['type'] == 3:
        content_type = 7
        objectId_messageId = ''
    elif cur[i]['body2']['type'] == 5:
        content_type = 1
        objectId_messageId = ''
    elif cur[i]['body2']['type'] == 6:
        content_type = 8
        objectId_messageId = ''
    elif cur[i]['body2']['type'] == 7:
        content_type = 7
        objectId_messageId = ''
    elif cur[i]['body2']['type'] == 907:
        content_type = 3
        objectId_messageId = ''
        body2_content = f"{cur[i]['body2']['fromUserId']}|{cur[i]['body2']['toUserId']}"
    elif cur[i]['body2']['type'] == 904:
        content_type = 4
        objectId_messageId = ''
        body2_content = f"{cur[i]['body2']['toUserId']}"
    elif cur[i]['body2']['type'] == 903:
        content_type = 6
        objectId_messageId = ''
        body2_content = f"{cur[i]['body2']['fromUserId']}"
    elif cur[i]['body2']['type'] == 94:
        content_type = 2
        objectId = f"{cur[i]['body2']['objectId']}"
        data = json.loads(objectId)
        objectId_messageId = data['messageId']
        print(f'objectId_messageId: {objectId_messageId}')
    else:
        content_type = 9999
        objectId_messageId = ''
        print("content_type error!")
    
    try:
        sql3 = f"""INSERT INTO muc_storage(chat_content,create_time,room_id,room_name,account_type,user_id,user_name,nick_name,room_type,content_type,channel_account,uuId,body2_messageId,objectId_messageId)
                        VALUES ('{body2_content}','{create_time}','{room_jid}','{room_name}',{account_type},{user_id},'{user_name}','{nick_name}',{room_type},{content_type},'{channel_account}',{uuId},'{body2_messageId}','{objectId_messageId}')"""
        sqlcursor.execute(sql3)
        db.commit()
        print(sql3)

    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()
        print(f"Error: {str(e)}")
        break
   
# 关闭数据库连接
db.close()