# This file contains all forms

from flask_wtf import FlaskForm
from wtforms.fields import (StringField, PasswordField, BooleanField,
                            SubmitField, SelectField, FileField,
                            TextAreaField)
from wtforms.validators import (DataRequired, Required, ValidationError,
                                Email, EqualTo)
from app_folder.models import User, Category, Location


# Form for signing in
class Login_form(FlaskForm):
    username = StringField('Логин', validators = [DataRequired()])
    password = PasswordField('Пароль', validators = [DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class Add_request_form(FlaskForm):
    categories = [(c.id, c.name) for c in Category.query.all()]
    categories.insert(0, (0, 'Выберите категорию'))
    category = SelectField('Категория товара', choices = categories, validators = [Required()], coerce = int)
    productname = StringField('Название продукта', validators = [DataRequired()])
    submit = SubmitField('Добавить товар')


class Add_offer_form(FlaskForm):
    categories = [(c.id, c.name) for c in Category.query.all()]
    categories.insert(0, (0, 'Выберите категорию'))
    category = SelectField('Категория товара', choices = categories, validators = [Required()], coerce = int)
    productname = StringField('Название продукта', validators = [DataRequired()])
    photo = FileField('Прикрепить фото')
    submit = SubmitField('Добавить товар')


class Register_form(FlaskForm):
    locations = [(l.id, l.name) for l in Location.query.all()]
    locations.insert(0, (0, 'обжага, общажка, общажечка'))
    location = SelectField('Общежитие', choices = locations, validators = [Required()], coerce = int)
    username = StringField('Логин', validators = [DataRequired()])
    first_name = StringField('Имя', validators = [DataRequired()])
    last_name = StringField('Фамилия', validators = [DataRequired()])
    email = StringField('email', validators = [DataRequired(), Email()])
    password = PasswordField('Пароль', validators = [DataRequired()])
    repeat_password = PasswordField('Повторите пароль', validators = [DataRequired(), EqualTo('password')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Продолжить регистрацию')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('Данный email уже занят')


class Search_form(FlaskForm):
    categories = [(c.id, c.name) for c in Category.query.all()]
    categories.insert(0, (0, 'Выберите категорию'))
    category = SelectField('Категория', choices = categories, coerce = int)
    locations = [(l.id, l.name) for l in Location.query.all()]
    locations.insert(0, (0, 'обжага, общажка, общажечка'))
    location = SelectField('Общежитие', choices = locations, coerce = int)
    productname = StringField('Название')
    submit = SubmitField('Найти')


class Edit_product_form(FlaskForm):
    categories = [(c.id, c.name) for c in Category.query.all()]
    categories.insert(0, (0, 'Выберите категорию'))
    category = SelectField('Категория товара', choices = categories, validators = [Required()], coerce = int)
    productname = StringField('Название продукта', validators = [DataRequired()])
    photo = FileField('Прикрепить фото')
    submit = SubmitField('Сохранить изменения')


class Edit_profile_form(FlaskForm):
    locations = [(l.id, l.name) for l in Location.query.all()]
    locations.insert(0, (0, 'обжага, общажка, общажечка'))
    location = SelectField('Общежитие', choices = locations, validators = [Required()], coerce = int)
    username = StringField('Логин', validators = [DataRequired()])
    first_name = StringField('Имя', validators = [DataRequired()])
    last_name = StringField('Фамилия', validators = [DataRequired()])
    email = StringField('email', validators = [DataRequired(), Email()])
    submit = SubmitField('Сохранить изменения')


class Send_message_form(FlaskForm):
    textarea = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Отправить')
