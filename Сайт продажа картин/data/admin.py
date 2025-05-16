from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms import EmailField
from wtforms.validators import DataRequired


class AdminForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    admin_status = EmailField('Привилегия пользователя (значения: ADMIN или любой набор символов)', validators=[DataRequired()])
    submit = SubmitField('Изменить')


class AddForm(FlaskForm):
    name = EmailField('Название картины', validators=[DataRequired()])
    more = PasswordField('Описание', validators=[DataRequired()])
    price = PasswordField('Цена', validators=[DataRequired()])
    img = PasswordField('Путь к изображению', validators=[DataRequired()])
    link = PasswordField('Ссылка', validators=[DataRequired()])
    submit = SubmitField('Добавить товар')


class RemoveForm(FlaskForm):
    name = EmailField('Название картины', validators=[DataRequired()])
    submit = SubmitField('Удалить товар')
