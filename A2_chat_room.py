# insert chat_room 
# insert im_mapping

import pymongo
import json
import html
from pymongo import MongoClient
import pymysql
# from datetime import datetime
import datetime
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
myclient = pymongo.MongoClient(env_mongodb_url)

# shiku_room
mydb = myclient["imRoom"]
mycol = mydb["shiku_room"]

eight_hours = datetime.timedelta(hours=8)

# 示例日期时间字符串
start_date_time_string = env_start_time
end_date_time_string = env_end_time

# 使用strptime()方法将日期时间字符串解析为日期时间对象
# start_dt_object = datetime.datetime.strptime(start_date_time_string, '%Y-%m-%d %H:%M:%S.%f')
# end_dt_object = datetime.datetime.strptime(end_date_time_string, '%Y-%m-%d %H:%M:%S.%f')

start_dt_object = datetime.datetime.strptime(start_date_time_string, '%Y-%m-%d')
end_dt_object = datetime.datetime.strptime(end_date_time_string, '%Y-%m-%d')

# 使用timestamp()方法将日期时间对象转换为时间戳
start_timestamp = start_dt_object.timestamp()
end_timestamp = end_dt_object.timestamp()

# start_timestamp = start_dt_object.timestamp() - eight_hours.total_seconds()
# end_timestamp = end_dt_object.timestamp() - eight_hours.total_seconds()

# start_timestamp = start_dt_object.timestamp()
# end_timestamp = end_dt_object.timestamp()

# print(f"start_timestamp:{start_timestamp}")
# print(f"end_timestamp:{end_timestamp}")

# 濾時間
#大於等於start_time 小於end_time
query = {"createTime" : {"$gte":start_timestamp,"$lt":end_timestamp}}
cur = mycol.find(query).sort([("createTime", pymongo.ASCENDING)])

# 總數
mongocount = cur.count()
print(mongocount)


# ======================== mysql env
db = pymysql.connect(host=f'{env_url}',
                     user=f'{env_user}',
                     password=f'{env_password}',
                     database=f'{env_database}')

cursor = db.cursor()



# print(cur)
for n in range(0,mongocount):

    current_timestamp = cur[n]['createTime']
    eight_hours = datetime.timedelta(hours=8)
    new_timestamp = current_timestamp 
    create_time = datetime.datetime.fromtimestamp(new_timestamp)

    im_room_id = cur[n]['_id']
    im_jid = cur[n]['jid']
    user_count = cur[n]['userSize']
    # 加入 im_room_id,im_jid 10/5
    inputdb = f"'{cur[n]['name']}','{create_time}',1,'/1687162246486.jpg',0,{user_count},'zlcai',0,{cur[n]['userId']},'{im_room_id}','{im_jid}','{create_time}'"
    print(inputdb)
    
    # 塞chat_room
    # 加入 im_room_id,im_jid 10/5
    sql = f"""INSERT INTO chat_room(room_name,create_time,type,room_icon,content_id,user_count,channel_account,room_mute_type,user_id,im_room_id,jid,update_time)
            VALUES ({inputdb})"""
    # room_id
    sql3 = f"""INSERT INTO im_mapping(room_id,im_room_id,im_jid)
                    VALUES ({n+1},'{im_room_id}','{im_jid}')"""

    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()

        # 执行sql语句
        cursor.execute(sql3)
        # 提交到数据库执行
        db.commit()

    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()
        print(f"Error: {str(e)}")
   
# 关闭数据库连接
db.close()