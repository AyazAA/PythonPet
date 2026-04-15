from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    name = StringField('ФИО', validators =[DataRequired(), Length(2, 50)])
    login = StringField('Логин', validators =[DataRequired(), Length(2, 20)])
    password = PasswordField('Пароль', validators =[DataRequired(), Length(2, 200)])
    confirm_password = PasswordField('Подтвердите пароль', validators =[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators =[DataRequired(), Length(2, 20)])
    password = PasswordField('Пароль', validators =[DataRequired(), Length(2, 200)])
    remember = BooleanField('Запомнить')
    submit = SubmitField('Войти')

class AuthorForm(FlaskForm):
    author = SelectField('author', choices=[], render_kw={"class": "form-control"})
