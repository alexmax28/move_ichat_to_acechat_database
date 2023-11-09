
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

# create_table_room_user_test
create_table_room_user_test = '''
CREATE TABLE room_user_test (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50),
    room_id VARCHAR(50),
    create_time datetime,
    leave_time datetime
);
'''
# create_table_muc_storage
create_table_muc_storage = '''
CREATE TABLE muc_storage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chat_content VARCHAR(2048),
    create_time datetime,
    room_id VARCHAR(50),
    room_name VARCHAR(50),
    account_type INT(11),
    user_id bigint(20),
    user_name VARCHAR(50),
    nick_name VARCHAR(50),
    room_type INT(11),
    content_type INT(11),
    channel_account VARCHAR(50),
    uuId VARCHAR(128),
    body2_messageId VARCHAR(128),
    objectId_messageId VARCHAR(128)
);
'''
# sql3 = f"ALTER TABLE aaa ADD body2_messageId varchar(255) DEFAULT NULL;"

# sql4 = f"ALTER TABLE aaa ADD objectId_messageId varchar(255) DEFAULT NULL;"

# ================================== 舊版chat_friend
# # create_table_chat_friend
# create_table_chat_friend = '''
# CREATE TABLE chat_friend (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id_1 int(20),
#     user_id_2 int(20),
#     create_time datetime,
#     check_flag int(11),
#     remark_1 VARCHAR(128),
#     remark_2 VARCHAR(128)
# );
# '''

create_table_chat_friend_test = '''
CREATE TABLE `chat_friend_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id_1` int(20) DEFAULT NULL,
  `user_id_2` int(20) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `check_flag` int(11) DEFAULT NULL,
  `remark_1` varchar(128) DEFAULT NULL,
  `remark_2` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
'''

# =================================================================  9/8新增
create_table_chat_friend = '''
CREATE TABLE `chat_friend` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id_1` bigint(20) NOT NULL,
  `user_id_2` bigint(20) NOT NULL,
  `create_time` datetime DEFAULT NULL,
  `check_flag` int(11) DEFAULT NULL,
  `remark_1` varchar(128) DEFAULT NULL,
  `remark_2` varchar(128) DEFAULT NULL,
  `room_id` bigint(20) DEFAULT NULL COMMENT '群組ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `chat_friend_UN` (`user_id_1`,`user_id_2`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
'''

create_table_chat_record = '''
CREATE TABLE `chat_record` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `chat_content` varchar(2048) DEFAULT NULL,
  `create_time` datetime(3) DEFAULT NULL,
  `room_id` bigint(20) DEFAULT NULL,
  `room_name` varchar(50) DEFAULT NULL,
  `account_type` int(11) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `user_name` varchar(50) DEFAULT NULL,
  `nick_name` varchar(50) DEFAULT NULL,
  `room_type` int(11) DEFAULT NULL,
  `content_type` int(11) DEFAULT NULL,
  `channel_account` varchar(50) DEFAULT NULL,
  `uuId` varchar(128) DEFAULT NULL,
  `body2_messageId` varchar(255) DEFAULT NULL,
  `objectId_messageId` varchar(255) DEFAULT NULL,
  `read_destory_status` int(11) unsigned DEFAULT '0' COMMENT '閱後消毀狀態',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
'''
# 10/5 新增 im_room_id , jid 欄位
create_table_chat_room = '''
CREATE TABLE `chat_room` (
  `room_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '群組ID',
  `room_name` varchar(50) DEFAULT NULL COMMENT '群組名稱',
  `create_time` datetime DEFAULT NULL,
  `type` int(11) DEFAULT NULL COMMENT '0-私聊,1-群聊',
  `room_icon` varchar(50) DEFAULT NULL,
  `content_id` bigint(20) DEFAULT NULL COMMENT '最後一筆聊天訊息',
  `user_count` int(11) DEFAULT NULL,
  `channel_account` varchar(50) DEFAULT NULL,
  `room_mute_type` int(11) DEFAULT NULL COMMENT '群禁言狀態: 0:未禁言 1:禁言',
  `user_id` int(11) DEFAULT NULL COMMENT '群主ID',
  `room_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '群組狀態: 0-正常，1-鎖定',
  `room_description` varchar(100) DEFAULT NULL COMMENT '群組描述',
  `update_time` datetime DEFAULT NULL COMMENT '更新時間',
  `im_room_id` varchar(100) DEFAULT NULL,
  `jid` varchar(100) DEFAULT NULL,
  `share_file_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '群共享文件開關 0:關 1:開',
  PRIMARY KEY (`room_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
'''

create_table_chat_user = '''
CREATE TABLE `chat_user` (
  `user_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) DEFAULT NULL COMMENT '帳號',
  `password` varchar(128) DEFAULT NULL,
  `nick_name` varchar(50) DEFAULT NULL,
  `is_online` int(11) DEFAULT NULL COMMENT '是否在線',
  `type` int(11) DEFAULT NULL COMMENT '帳號類型 0:會員 1:管理員',
  `status` int(11) DEFAULT NULL COMMENT '狀態 0:停用 1:啟用',
  `phone` varchar(20) DEFAULT NULL,
  `tId` varchar(512) DEFAULT NULL,
  `device` int(11) DEFAULT NULL,
  `firebase_token` varchar(512) DEFAULT NULL,
  `channel_account` varchar(50) DEFAULT NULL,
  `ip` varchar(50) DEFAULT NULL,
  `last_online_time` datetime DEFAULT NULL,
  `tId_android` varchar(512) DEFAULT NULL,
  `tId_ios` varchar(512) DEFAULT NULL,
  `data_type` int(11) NOT NULL DEFAULT '0' COMMENT '外部倒入資料 0:內部 1:外部',
  `create_time` datetime DEFAULT NULL COMMENT '創建時間',
  `update_time` datetime DEFAULT NULL,
  `show_telephone` int(11) DEFAULT '1' COMMENT '誰可以看到我的手機號碼,0:所有人不允許,1:所有人允許,2:所有好友允許',
  `is_vibration` int(11) DEFAULT '1' COMMENT '消息來時震動,0:關閉,1:開啟',
  `multiple_devices` int(11) DEFAULT '1' COMMENT '支持多設備登入,0:關閉,1:開啟',
  `refresh_tId` varchar(512) DEFAULT NULL,
  `refresh_ios_tId` varchar(512) DEFAULT NULL,
  `refresh_android_tId` varchar(512) DEFAULT NULL,
  `area_code` varchar(10) DEFAULT NULL COMMENT '區碼',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `chat_user_UN` (`user_name`,`area_code`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
'''

create_table_im_mapping = '''
CREATE TABLE `im_mapping` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `room_id` bigint(20) NOT NULL,
  `im_room_id` varchar(100) NOT NULL,
  `im_jid` varchar(100) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `im_mapping_id_IDX` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
'''

# ===================================================== 測試用新增 chat_room_user_test 之後 chat_room_user 欄位要改成這樣


# chart_room_user_test  room_id 欄位改型態 varchar(100)
create_table_chat_room_user = '''
CREATE TABLE `chat_room_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) DEFAULT NULL,
  `room_id` bigint(20) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `leave_time` datetime DEFAULT NULL,
  `inviter` varchar(50) DEFAULT NULL,
  `inviter_type` int(11) DEFAULT NULL,
  `mute_type` int(11) DEFAULT NULL,
  `notification_flag` int(11) NOT NULL DEFAULT '0',
  `room_background_img` varchar(128) DEFAULT NULL COMMENT '聊天室背景圖片',
  `clean_time` datetime(3) DEFAULT NULL COMMENT '聊天清空時間',
  `read_destory_status` int(11) DEFAULT '0' COMMENT '閱後消毀開關 0:關閉 1:開啟',
  `room_user_type` int(11) NOT NULL DEFAULT '0' COMMENT '0:一般用戶 1:房間管理員',
  PRIMARY KEY (`id`),
  UNIQUE KEY `chat_room_user_UN` (`user_id`,`room_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
'''

try:
        # 执行sql语句
        sqlcursor.execute(create_table_room_user_test)
        # 提交到数据库执行
        db.commit()

        sqlcursor.execute(create_table_muc_storage)
        db.commit()

        sqlcursor.execute(create_table_chat_friend_test)
        db.commit()


        # chat_friend
        sqlcursor.execute(create_table_chat_friend)
        db.commit()
        
        # chat_record
        sqlcursor.execute(create_table_chat_record)
        db.commit()

        # chat_room
        sqlcursor.execute(create_table_chat_room)
        db.commit()
        
        # chat_user
        sqlcursor.execute(create_table_chat_user)
        db.commit()

        # im_mapping
        sqlcursor.execute(create_table_im_mapping)
        db.commit()

        # chat_room_user
        sqlcursor.execute(create_table_chat_room_user)
        db.commit()


        # # 測試用新增 chat_room_user_test 之後 chat_room_user 欄位要改成這樣  room_id 欄位改型態 varchar(100)
        # sqlcursor.execute(create_table_chat_room_user_test)
        # db.commit()


        # print(sql3)
        # sqlcursor.execute(sql3)
        # db.commit()
    
        
        # print(sql4)
        # sqlcursor.execute(sql4)
        # db.commit()
      

        
except:
        # 如果发生错误则回滚
        db.rollback()
   
# 关闭数据库连接
db.close()