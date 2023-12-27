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
env_channel_account = os.getenv("CHANNEL_ACCOUNT")
# ============== mongo
myclient = pymongo.MongoClient(env_mongodb_url)
mydb = myclient["imapi"]
mycol = mydb["user"]



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

print(f"start_timestamp:{start_timestamp}")
print(f"end_timestamp:{end_timestamp}")



# 濾時間
#大於等於start_time 小於end_time
query = {"createTime" : {"$gte":start_timestamp,"$lt":end_timestamp}}
cur = mycol.find(query).sort([("createTime", pymongo.ASCENDING)])

# 總數
mongocount = cur.count()
print(mongocount)

# ========================mysql env
db = pymysql.connect(host=f'{env_url}',
                     user=f'{env_user}',
                     password=f'{env_password}',
                     database=f'{env_database}')
cursor = db.cursor()



for i in range(0,mongocount):
    current_timestamp = cur[i]['createTime']
    eight_hours = datetime.timedelta(hours=8)
    new_timestamp = current_timestamp
    create_time = datetime.datetime.fromtimestamp(new_timestamp)

    if cur[i]['areaCode'] == '000':
        if "userAccount" not in cur[i]:
            continue

        inputdb = f"'{cur[i]['userAccount']}','{cur[i]['password']}','{cur[i]['nickname']}','{create_time}',1,'{create_time}',1,'acechat',1"

        sql = f"""INSERT INTO system_user(user_name,password,nick_name,create_time,role_id,update_time,status,channel_account,data_type)
        VALUES ({inputdb})"""

        try:
        # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            print(sql)
        except:
            # 如果发生错误则回滚
            db.rollback()
            print("error!")







# # 新增測試表 chat_user
#     sql = f"""INSERT INTO chat_user(user_id,user_name,password,nick_name,create_time,is_online,type,status,phone,tId,device,firebase_token,channel_account,ip,tId_android,tId_ios,data_type,area_code)
#             VALUES ({inputdb})"""

#     print(sql)

#     try:
#         # 执行sql语句
#         cursor.execute(sql)
#         # 提交到数据库执行
#         db.commit()
#     except:
#         # 如果发生错误则回滚
#         db.rollback()
    
# 关闭数据库连接
db.close()