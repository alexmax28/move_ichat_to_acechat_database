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
# # # ========================mongo
# myclient = pymongo.MongoClient(env_mongodb_url)

# mydb = myclient["imapi"]
# mycol = mydb["u_friends"]
# cur = mycol.find()
# count = mycol.count()


# ========================sql env
db = pymysql.connect(host=f'{env_url}',
                     user=f'{env_user}',
                     password=f'{env_password}',
                     database=f'{env_database}')


cursor = db.cursor()

dict = {}
arr_list = []
set_list = set()
final_list = []
# create_time = datetime.now()
    # toUserId = cur[i]["toUserId"]
    # userId = cur[i]["userId"]
time_difference = timedelta(hours=8)

start_time_o = env_start_time
end_time_o = env_end_time

date_format = "%Y-%m-%d %H:%M:%S.%f"
# start_time = datetime.strptime(start_time_o, date_format) - time_difference
# end_time = datetime.strptime(end_time_o, date_format) - time_difference

start_time = datetime.strptime(start_time_o, date_format)
end_time = datetime.strptime(end_time_o, date_format) 

# print(start_time)
# print(end_time)

try:
        # sql4 = f"""select user_id_1,user_id_2,create_time,check_flag,remark_1,remark_2
        #             from chat_friend_test"""
        sql3 = f"""select user_id_1,user_id_2,create_time
                    from chat_friend_test
                    where create_time >='{start_time}' AND create_time <'{end_time}'
                    order by user_id_1 ASC; """
        # 执行sql语句
        cursor.execute(sql3)
       
        # 提交到数据库执行
        db.commit()
        

        resjoin = cursor.fetchall()
        print(len(resjoin))
        # print(resjoin)
        for a in range(len(resjoin)):
            #  print(f"{resjoin[a][0]},{resjoin[a][1]}")
            # print(f"0: {type(resjoin[a][0])}")
            # print(f"1: {type(resjoin[a][1])}")
            id_1 = resjoin[a][0]
            id_2 = resjoin[a][1]
            create_time = resjoin[a][2]
            # print(create_time)
            if id_1 < id_2:
                id_str = f"{id_1},{id_2},{create_time}"
                set_list.add(id_str)
            else:
                id_str = f"{id_2},{id_1},{create_time}"
                set_list.add(id_str)
            # print(set_list)
        
                  
except Exception as e:
            # 如果发生错误则回滚
            db.rollback()
            print(f"Error: {str(e)}")
# print(set_list)
for ans in set_list:
    str = f"{ans}"
    fstr = str.split(",")
    final_list.append(fstr)
# print(final_list)    
# print(len(final_list))
for b in range(0,len(final_list)):
     
    id_1 = final_list[b][0]
    id_2 = final_list[b][1]
    createTtime = final_list[b][2]
    # print(f"id_1: {id_1}")
    # print(f"type: {type(id_1)}")
    # print(f"id_2: {id_2}")

    try:
        sql3 = f"""INSERT INTO chat_friend(user_id_1,user_id_2,create_time,check_flag,remark_1,remark_2)
                        VALUES ({int(id_1)},{int(id_2)},'{createTtime}',1,NULL,NULL); """
        
        print(sql3)
        cursor.execute(sql3)
        db.commit()
        
    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()
        print(f"Error: {str(e)}")

# 关闭数据库连接
db.close()
   



