'''
Author: your name
Date: 2021-12-23 13:06:28
LastEditTime: 2021-12-25 16:34:34
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /python3-sql/utils.py
'''
import MySQLdb
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

class MysqlSearch(object):
  def __init__(self) -> None:
      super().__init__()
      self.get_conn()
      
  def get_conn(self):
    try:
      self.conn = MySQLdb.connect(
        host = '127.0.0.1',
        user = 'root',
        password = 'root',
        db = 'school',
        port = 3306,
        charset = 'utf8'
      )
    except MySQLdb.Error as e:
      print('Error: {}'.format(e))

  def close_conn(self):
    try:
      if self.conn:
        self.conn.close()
    except MySQLdb.Error as e:
      print('Error: {}'.format(e))

  def get_one(self):
    # sql
    sql = 'SELECT * from `students` WHERE `sex` = %s ORDER BY `id` DESC;'
    # find cursor
    cursor = self.conn.cursor()
    # execute sql
    cursor.execute(sql, ('男', ))
    # print(cursor.rowcount)
    # result
    # result = cursor.fetchone()
    result = dict(zip([k[0] for k in cursor.description], cursor.fetchone()))
    # print, result type is tuple
    # print('result:', result)
    # close connect
    cursor.close()
    self.close_conn()
    return result

  def get_more(self):
    # sql
    sql = 'SELECT * from `students` WHERE `sex` = %s ORDER BY `id` DESC;'
    # find cursor
    cursor = self.conn.cursor()
    # execute sql
    cursor.execute(sql, ('男', ))
    # print(cursor.rowcount)
    # result
    # result = cursor.fetchone()
    result = [
      dict(zip([k[0] for k in cursor.description], row))
      for row in cursor.fetchall()
    ]
    # print, result type is tuple
    # print('result:', result)
    # close connect
    cursor.close()
    self.close_conn()
    return result

  def get_more2(self, page, page_size):
    offset = (page - 1) * page_size
    # sql
    sql = 'SELECT * from `students` WHERE `sex` = %s ORDER BY `id` DESC LIMIT %s, %s;'
    # find cursor
    cursor = self.conn.cursor()
    # execute sql
    cursor.execute(sql, ('男', offset, page_size))
    # print(cursor.rowcount)
    # result
    # result = cursor.fetchone()
    result = [
      dict(zip([k[0] for k in cursor.description], row))
      for row in cursor.fetchall()
    ]
    # print, result type is tuple
    # print('result:', result)
    # close connect
    cursor.close()
    self.close_conn()
    return result

  def add_one(self):
    try:
      sql = 'INSERT INTO `students` (`id`, `name`, `nickname`, `sex`) VALUE (%s, %s, %s, %s);'
      cursor = self.conn.cursor()
      cursor.execute(sql, (7, 'ohayo', '裤裆藏地雷', '女'))
      self.conn.commit()
      cursor.close()
    except:
      self.conn.rollback()

    self.conn.close()

class TestMongo(object):
  def __init__(self) -> None:
      super().__init__()
      self.client = MongoClient()
      self.db = self.client['demo']

  def add_one(self):
    post = {
      'sn': 9,
      'name': 'koa1'
    }
    return self.db.user.insert_one(post)

  def get_one(self):
    return self.db.user.find_one()

  def get_more(self):
    return self.db.user.find({'name': 'express'})

  def get_from_oid(self, oid):
    return self.db.user.find_one({'_id': ObjectId(oid)})

  def update_one(self):
    # return self.db.user.update_one({'age': 20}, {'$inc': {'age': 10}})
    # return self.db.user.update_one({'name': 'koa1'}, {'$set': {'name': 'koa111111--'}})
    return self.db.user.update_many({}, {'$inc': {'age': 10}})

  def delete(self):
    # return self.db.user.delete_one({'name': 'koa111111--'})
    return self.db.user.delete_many({'name': 'express'})