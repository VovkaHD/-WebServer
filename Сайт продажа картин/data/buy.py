from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms import EmailField
from wtforms.validators import DataRequired


class BuyForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    phone = EmailField('Телефонный номер', validators=[DataRequired()])
    submit = SubmitField('Оформить заказ')
