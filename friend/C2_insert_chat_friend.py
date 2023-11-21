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
final_list = []
obj = {}

# now_time = datetime.now() - timedelta(days=1)
    # toUserId = cur[i]["toUserId"]
    # userId = cur[i]["userId"]
time_difference = timedelta(hours=8)

start_time_o = env_start_time
end_time_o = env_end_time

# date_format = "%Y-%m-%d %H:%M:%S.%f"
date_format = "%Y-%m-%d"
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
        # print(len(resjoin))
        # print(resjoin)
        if len(resjoin) == 0:
            print("insert chat_friend count : 0")
        else:
            for a in range(len(resjoin)):
                id_1 = resjoin[a][0]
                id_2 = resjoin[a][1]
                create_time = resjoin[a][2]
                # print(create_time)
                if id_1 < id_2:
                    id_str_key = f"{id_1},{id_2}"
                    obj[id_str_key] = [id_1,id_2,create_time]
                else:
                    id_str_key = f"{id_2},{id_1}"
                    obj[id_str_key] = [id_2,id_1,create_time]
            # print(obj)
            for item in obj.values():
                final_list.append(item)
            print(final_list[0])

            
# 11/18 把這個迴圈從外面移到裡面
            for b in final_list:
                id_1 = b[0]
                id_2 = b[1]
                createTtime = b[2]

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
# ================================
        
                  
except Exception as e:
            # 如果发生错误则回滚
            db.rollback()
            print(f"Error: {str(e)}")


# 关闭数据库连接
db.close()
   



