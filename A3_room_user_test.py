
# shiku_room_member > room_user_test_3
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

# ========================sql env
db = pymysql.connect(host=f'{env_url}',
                     user=f'{env_user}',
                     password=f'{env_password}',
                     database=f'{env_database}')


sqlcursor = db.cursor()


mydb = myclient["imRoom"]

# shiku_room_member
mycol2 = mydb["shiku_room_member"]

eight_hours = datetime.timedelta(hours=8)

# 示例日期时间字符串
start_date_time_string = env_start_time
end_date_time_string = env_end_time
# 使用strptime()方法将日期时间字符串解析为日期时间对象
start_dt_object = datetime.datetime.strptime(start_date_time_string, '%Y-%m-%d %H:%M:%S.%f')
end_dt_object = datetime.datetime.strptime(end_date_time_string, '%Y-%m-%d %H:%M:%S.%f')
# 使用timestamp()方法将日期时间对象转换为时间戳
start_timestamp = start_dt_object.timestamp()
end_timestamp = end_dt_object.timestamp()

# start_timestamp = start_dt_object.timestamp() - eight_hours.total_seconds()
# end_timestamp = end_dt_object.timestamp() - eight_hours.total_seconds()
print(f"start_timestamp:{start_timestamp}")
print(f"end_timestamp:{end_timestamp}")

# 濾時間
#大於等於start_time 小於end_time
query = {"createTime" : {"$gte":start_timestamp,"$lt":end_timestamp}}
cur = mycol2.find(query).sort([("createTime", pymongo.ASCENDING)])

# 總數
mongocount = cur.count()
print(mongocount)


for i in range(0,mongocount):
    user_id = cur[i]['userId']
    roomId = cur[i]['roomId']
    # create_time = datetime.fromtimestamp(cur[i]['createTime'])
    # leave_time = datetime.fromtimestamp(cur[i]['createTime'])

    create_time_1 = cur[i]['createTime']
    leave_time_1 = cur[i]['createTime']
    eight_hours = datetime.timedelta(hours=8)
    new_create_time_timestamp = create_time_1
    new_leave_time_timestamp = leave_time_1
    create_time = datetime.datetime.fromtimestamp(new_create_time_timestamp)
    leave_time = datetime.datetime.fromtimestamp(new_leave_time_timestamp)



    print(f"user_id: {cur[i]['userId']}")
    print(f"roomId:{cur[i]['roomId']}")
    print(f"create_time:{create_time}")
    print(f"leave_time:{leave_time}")

    sql = f"""INSERT INTO room_user_test(user_id,room_id,create_time,leave_time)
            VALUES ('{user_id}','{roomId}','{create_time}','{leave_time}')"""
    
    try:
        # 执行sql语句
        sqlcursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        print(sql)

    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()
        print(f"Error: {str(e)}")
   
# 关闭数据库连接
db.close()    