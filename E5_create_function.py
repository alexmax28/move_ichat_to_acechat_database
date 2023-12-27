
# create_table_room_user_test  create_table_muc_storage
import pymongo
import json
import html
from pymongo import MongoClient
import pymysql
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()
# ============== ENV
env_url = os.getenv("DATABASE_URL")
env_user = os.getenv("USER")
env_password = os.getenv("PASSWORD")
env_database = os.getenv("DATABASE")

# # ========================sql 232
# db = pymysql.connect(host='192.168.100.232',
#                      user='root',

#                      password='XhR7r5yPBlmImHAD',
#                      database='iChat')

# ========================sql 210
# db = pymysql.connect(host='192.168.100.210',
#                      user='root',

#                      password='12345678',
#                      database='ichat')

# ========================sql env
db = pymysql.connect(host=f'{env_url}',
                     user=f'{env_user}',
                     password=f'{env_password}',
                     database=f'{env_database}')


sqlcursor = db.cursor()


# currval 
create_fn_currval='''
CREATE DEFINER=`root`@`%` FUNCTION `currval`(v_seq_name VARCHAR(50)) RETURNS int(11)
BEGIN
		declare value integer;
		set value = 0;
		select current_value into value  from sequence where name = v_seq_name;
		 return value;
END
'''

# nextval 
create_fn_nextval='''
CREATE DEFINER=`root`@`%` FUNCTION `nextval`(v_seq_name VARCHAR(50)) RETURNS int(11)
BEGIN
		update sequence set current_value = current_value + increment  where name = v_seq_name;
    return currval(v_seq_name);
END
'''

try:
        # currval
        sqlcursor.execute(create_fn_currval)
        db.commit()

        # nextval
        sqlcursor.execute(create_fn_nextval)
        db.commit()
      

        
except:
        # 如果发生错误则回滚
        db.rollback()
   
# 关闭数据库连接
db.close()