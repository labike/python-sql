'''
Author: labike ddmmy@hotmail.com
Date: 2022-06-12 11:04:21
LastEditors: labike ddmmy@hotmail.com
LastEditTime: 2022-06-13 10:36:59
FilePath: /python3-sql/utils2.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import MySQLdb

# from utils import MysqlSearch

# try:
#   conn = MySQLdb.connect(
#     host='127.0.0.1.',
#     user='root',
#     password='root',
#     db='news2',
#     port=3306,
#     charset='utf8'
#   )
#   cursor = conn.cursor()
#   cursor.execute('select * from `news` order by `created_at` desc;')
#   res = cursor.fetchone()
#   print(res)
#   cursor.close()
# except MySQLdb.Error as e:
#   print('Error: %s' % e)


class MySqlSearch(object):
  def __init__(self):
    self.get_conn()

  def get_conn(self):
    try:
      self.conn = MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        password= 'root',
        db='news',
        port=3306,
        charset='utf8'
      )
    except MySQLdb.Error as e:
      print('Error %s' % e)

  def close_conn(self):
    try:
      if self.conn:
        self.conn.close()
    except MySQLdb.Error as e:
      print('Error %s' % e)

  def get_one(self):
    # 准备sql
    sql = 'select * from `news` where `types`=%s order by `created_at` desc;'
    # 找到cursor
    cursor = self.conn.cursor()
    # 执行sql
    cursor.execute(sql, ('百度',))
    # 获取结果(tuple转dict)
    res = dict(zip([k[0] for k in cursor.description], cursor.fetchone()))
    # 处理数据
    # print(res['title'])
    # 关闭连接
    cursor.close()
    self.close_conn()
    return res

  def get_more(self):
    # 准备sql
    sql = 'select * from `news` where `types`=%s order by `created_at` desc;'
    # 获取cursor
    cursor = self.conn.cursor()
    # 执行sql
    cursor.execute(sql, ('新浪',))
    # 获取结果list
    res = [dict(zip([k[0] for k in cursor.description], row)) for row in cursor.fetchall()]
    # 关闭连接
    cursor.close()
    self.close_conn()
    return res

  def add_one(self):
    try:
      # sql
      sql = 'insert into `news`(`title`, `img_url`, `content`, `news_type`) value (%s, %s, %s, %s);'
      # 连接
      cursor = self.conn.cursor()
      # 执行sql
      cursor.execute(sql, ('我是koa', '1.png', 'xczc', '1'))
      #提交数据
      self.conn.commit()
      # 关闭连接
      cursor.close()
    except MySQLdb.Error as e:
      # 如果多条数据时有一条出错则进行回滚
      self.conn.rollback()

    self.close_conn()

def main():
  obj = MySqlSearch()
  # res = obj.get_one()
  # res = obj.get_more()
  # for item in res:
  #   print('res', item)
  obj.add_one()

if __name__ == '__main__':
  main()