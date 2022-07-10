'''
Author: your name
Date: 2021-12-25 19:36:54
LastEditTime: 2021-12-25 20:44:39
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /python3-sql/app2.py
'''
from datetime import datetime
from flask import Flask, render_template, flash, url_for, redirect
from flask_mongoengine import MongoEngine
from forms import NewsForm

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
  'db': 'news',
  'host': '127.0.0.1',
  'port': 27017
}
app.config['SECRET_KEY'] = '123456'
db = MongoEngine(app)

NEWS_TYPES = (
  ('推荐', '推荐'),
  ('新浪', '新浪'),
  ('腾讯', '腾讯'),
  ('百度', '百度')
)

class News(db.Document):
  title = db.StringField(required = True, max_length = 200)
  content = db.StringField(required = True)
  image = db.StringField()
  types = db.StringField(required = True, choices = NEWS_TYPES)
  is_valid = db.BooleanField(default = True)
  created_at = db.DateTimeField(default = datetime.now())
  updated_at = db.DateTimeField(default = datetime.now())

  meta = {
    'collection': 'news',
    'order': ['-created_at']
  }

@app.route('/')
def home():
  news_list = News.objects.filter(is_valid = True)
  return render_template('index.html', news_list = news_list)

@app.route('/cat/<name>/')
def cat(name):
  news_list = News.objects.filter(is_valid = True, types = name)
  return render_template('cat.html', news_list = news_list)

@app.route('/detail/<id>/')
def detail(id):
  obj = News.objects.filter(id = id).get_or_404()
  return render_template('detail.html', obj = obj)

@app.route('/admin')
@app.route('/admin/<int:page>')
def admin(page = None):
  if page is None:
    page = 1

  news_list = News.objects.paginate(page = page, per_page = 2)
  return render_template('admin/index.html', news_list = news_list, page = page)

@app.route('/admin/update/<id>/', methods = ['GET', 'POST'])
def update(id):
  obj = News.objects.get_or_404(id = id)
  form = NewsForm(obj = obj)
  if form.validate_on_submit():
    obj.title = form.title.data
    obj.content = form.content.data
    obj.image = form.image.data
    obj.types = form.types.data

  obj.save()
  flash('修改成功')
  redirect(url_for('admin'))
  return render_template('admin/update.html', form = form)

@app.route('/admin/add', methods = ['GET', 'POST'])
def add():
  form = NewsForm()
  if form.validate_on_submit():
    new_obj = News(
      title = form.title.data,
      content = form.content.data,
      image = form.image.data,
      types = form.types.data,
    )
    new_obj.save()
    flash('新增成功')
    redirect(url_for('admin'))
  return render_template('admin/add.html', form = form)

@app.route('/admin/delete/<id>', methods = ['POST'])
def delete(id):
  obj = News.objects.filter(id = id).first()
  if not obj:
    return 'no'

  obj.is_valid = False
  obj.save()
  # obj.delete()
  return 'yes'

if __name__ == '__main__':
  app.run(debug = True)
