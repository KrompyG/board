# This file contains all forms

from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Required

# Form for signing in
class LoginForm(FlaskForm):
    username = StringField('Логин', validators = [DataRequired()])
    password = PasswordField('Пароль', validators = [DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    
class AddProductForm(FlaskForm):
    categories = [(0, 'еда'),
                  (1, 'товары для дома'),
                  (2, 'одежда')]
                  # get this from db
    category = SelectField('Категория товара', choices = categories, validators = [Required()], coerce = int)
    productname = StringField('Название продукта', validators = [DataRequired()])
    photo = FileField('Прикрепить фото')
    submit = SubmitField('Добавить товар')
    