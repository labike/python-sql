'''
Author: your name
Date: 2021-12-23 15:08:58
LastEditTime: 2021-12-23 16:10:47
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /python3-sql/orm.py
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql://root:root@localhost/school')
Base = declarative_base()
Session = sessionmaker(bind=engine)

class News(Base):
  __tablename__ = 'news'
  id = Column(Integer, primary_key=True)
  title = Column(String(200), nullable=False)
  content = Column(String(2000), nullable=False)
  types = Column(String(10), nullable=False)
  image = Column(String(300), )
  author = Column(String(20), )
  view_counter = Column(Integer)
  created_at = Column(DateTime)
  updated_at = Column(DateTime)
  is_valid = Column(Boolean)

class OrmTest(object):
  def __init__(self) -> None:
      super().__init__()
      self.session = Session()

  def add_one(self):
    obj = News(
      title = '标题1',
      content = '内容1',
      types = '新浪'
    )

    self.session.add(obj)
    self.session.commit()
    return obj

  def add_more(self):
    obj = [
      News(
        title = '标题2',
        content = '内容2',
        types = '百度'
      ),
      News(
        title = '标题3',
        content = '内容3',
        types = '腾讯'
      ),
      News(
        title = '标题4',
        content = '内容4',
        types = '搜狐'
      )
    ]

    self.session.add_all(obj)
    self.session.commit()
    return obj

  def get_one(self):
    return self.session.query(News).get(5)

  def get_more(self):
    return self.session.query(News).filter_by(is_valid=True)

  def update_data(self):
    '''
    obj = self.session.query(News).get(id)
    if obj:
      obj.is_valid = 1
      self.session.add(obj)
      self.session.commit()
      return True
    return False
    '''

    obj_list = self.session.query(News).filter_by(is_valid=True)
    for item in obj_list:
      item.is_valid = 0
      self.session.add(item)
    self.session.commit()

  def del_one(self, id):
    obj = self.session.query(News).get(id)
    self.session.delete(obj)
    self.session.commit()