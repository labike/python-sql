'''
Author: your name
Date: 2021-12-25 16:42:15
LastEditTime: 2021-12-25 18:51:06
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /python3-sql/odm.py
'''
from mongoengine import EmbeddedDocument, connect, Document, \
  StringField, IntField, FloatField, ListField, EmbeddedDocumentField

connect('students')

SEX = (
  ('male', '男'),
  ('female', '女')
)

class Grades(EmbeddedDocument):
  name = StringField(required = True)
  score = FloatField(required = True)

class Student(Document):
  name = StringField(max_length = 32, required = True)
  age = IntField(required = True)
  grade = FloatField()
  grades = ListField(EmbeddedDocumentField(Grades))
  sex = StringField(choices = SEX, required = True)
  address = StringField()

  meta = (
    collection: 'students'
  )

class TestModel(object):
  def __init__(self) -> None:
      super().__init__()

  def add_one(self):
    english = Grades(name = '英语', score = 100)
    math = Grades(name = '数学', score = 20)

    obj = Student(
      name = 'koa',
      age = 20,
      sex = 'male',
      grades = [english, math]
    )

    obj.remark = 'remark'
    obj.save()
    return obj

  def get_one(self):
    return Student.objects.first()

  def get_more(self):
    return Student.object.all()

  def get_from_id(self, id):
    return Student.objects.filter(id = id).first()

  def update(self):
    Student.objects.filter(sex = 'male').update(inc__age = 10)
    Student.objects.filter(sex = 'male').update_one(inc__age = 10)

  def delete(self):
    Student.objects.filter(sex = 'male').first().delete()
    Student.objects.filter(sex = 'male').delete()