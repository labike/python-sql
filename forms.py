'''
Author: your name
Date: 2021-12-24 09:35:46
LastEditTime: 2021-12-24 11:23:43
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /python3-sql/forms.py
'''
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField 
from wtforms.validators import DataRequired

class NewsForm(FlaskForm):
  title = StringField(
    label = '标题',
    validators = [DataRequired('请输入标题')],
    description = '请输入标题',
    render_kw = {'required': 'required', 'class': 'form-control'}
  )

  content = TextAreaField(
    label = '内容',
    validators = [DataRequired('请输入内容')],
    description = '请输入内容',
    render_kw = {'required': 'required', 'class': 'form-control'}
  )

  types = SelectField(
    '类型',
    choices = [('推荐', '推荐'), ('新浪', '新浪'), ('腾讯', '腾讯'), ('百度', '百度')]
  )

  image = StringField(
    label = '图片',
    description = '图片地址',
    render_kw = {'required': 'required', 'class': 'form-control'}
  )

  submit = SubmitField('提交')