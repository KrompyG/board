# This file contains all forms

from flask_wtf import FlaskForm
from wtforms.fields import (StringField, PasswordField, BooleanField,
                            SubmitField, SelectField, FileField)
from wtforms.validators import (DataRequired, Required, ValidationError,
                                Email, EqualTo)
from app_folder.models import User

# Form for signing in
class Login_form(FlaskForm):
    username = StringField('Логин', validators = [DataRequired()])
    password = PasswordField('Пароль', validators = [DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    
class Add_product_form(FlaskForm):
    categories = [(0, 'еда'),
                  (1, 'товары для дома'),
                  (2, 'одежда')]
                  # get this from db
    category = SelectField('Категория товара', choices = categories, validators = [Required()], coerce = int)
    productname = StringField('Название продукта', validators = [DataRequired()])
    photo = FileField('Прикрепить фото')
    submit = SubmitField('Добавить товар')

class Register_form(FlaskForm):
    locations = [(0, '1-я Синичкина д.3 к.1А'),
                (1, '1-я Синичкина д.3 к.1'),
                (2, 'Энергетическая д.10'),
                (3, 'Энергетическая д.14'),
                (4, 'Энергетическая д.18')]
                #get from db
    location = SelectField('Общежитие', choices = locations, validators = [Required()], coerce = int)
    username = StringField('Логин', validators = [DataRequired()])
    email = StringField('email', validators = [DataRequired(), Email()])
    password = PasswordField('Пароль', validators = [DataRequired()])
    repeat_password = PasswordField('Повторите пароль', validators = [DataRequired(), EqualTo('password')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Продолжить регистрацию')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Данное имя пользователя уже занято')

    def validate_password(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('Данный email уже занят')