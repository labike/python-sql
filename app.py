'''
Author: your name
Date: 2021-12-23 12:51:07
LastEditTime: 2021-12-25 18:51:25
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /python3-sql/app.py
'''
from datetime import datetime
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import NewsForm
from utils import MysqlSearch, TestMongo
from orm import News, engine, OrmTest

'''
  obj = MysqlSearch()
  # result = obj.get_one()
  # result = obj.get_more()
  # result = obj.get_more2(3, 2)
  result = obj.add_one()
  print(result)
'''

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/news2'
app.config['SECRET_KEY'] = '123456'
db = SQLAlchemy(app)

class News(db.Model):
  __tablename__ = 'news'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200), nullable=False)
  content = db.Column(db.String(2000), nullable=False)
  types = db.Column(db.String(10), nullable=False)
  image = db.Column(db.String(300), )
  author = db.Column(db.String(20), )
  view_counter = db.Column(db.Integer)
  created_at = db.Column(db.DateTime)
  updated_at = db.Column(db.DateTime)
  is_valid = db.Column(db.Boolean)

  def __repr__(self) -> str:
      return '<News {}>'.format(self.title)

@app.route('/')
def home():
  news_list = News.query.filter_by(is_valid=1)
  return render_template('index.html', news_list = news_list)

@app.route('/cat/<name>')
def cat(name):
  news_list = News.query.filter(News.types == name)
  return render_template('cat.html', name=name, news_list = news_list)

@app.route('/detail/<int:id>/')
def detail(id):
  obj = News.query.get(id)
  return render_template('detail.html', id=id, obj = obj)

'''
后台
'''

@app.route('/admin/')
@app.route('/admin/<int:page>/')
def admin(page=None):
  if page is None:
    page = 1
  news_list = News.query.filter_by(is_valid = True).paginate(page=page, per_page=5)
  return render_template('admin/index.html', news_list = news_list)

@app.route('/admin/add/', methods = ('GET', 'POST'))
def add():
  form = NewsForm()
  if form.validate_on_submit():
    obj = News(
      title = form.title.data,
      content = form.content.data,
      types = form.types.data,
      image = form.image.data,
      created_at = datetime.now(),
      updated_at = datetime.now(),
      is_valid = 1
    )
    db.session.add(obj)
    db.session.commit()
    return redirect(url_for('admin'))
  return render_template('admin/add.html', form = form)

@app.route('/admin/update/<int:id>/', methods = ('GET', 'POST'))
def update(id):
  detail = News.query.get(id)
  if not detail:
    redirect(url_for('admin'))
  
  form = NewsForm(obj = detail)
  if form.validate_on_submit():
    detail.title = form.title.data
    detail.content = form.content.data
    detail.types = form.types.data
    detail.image = form.image.data

    db.session.add(detail)
    db.session.commit()
    return redirect(url_for('admin'))
  return render_template('admin/update.html', form = form)

@app.route('/admin/delete/<int:id>/', methods = ('GET', 'POST'))
def delete(id):
  obj = News.query.get(id)
  if not obj:
    return 'no'

  obj.is_valid = False
  db.session.add(obj)
  db.session.commit()
  return 'yes'


if __name__ == '__main__':
  app.run(debug=True)
  # News.metadata.create_all(engine)
  # obj = OrmTest()
  # result = obj.del_one(1)
  # print(result)
  '''
  if result:
    print('result id: {} => {}'.format(result.id, result.title))
  else:
    print('Not exists')
  '''

  '''
  for item in result:
    print('result id: {} => {}'.format(item.id, item.title))
  '''

  # result = obj.get_more()
  # for item in result:
  #   print(item)

