from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, logout_user, LoginManager
from app.forms import RegistrationForm, LoginForm
from ..extentions import db
from ..models.user import User
from flask_bcrypt import Bcrypt



user = Blueprint('user', __name__)

login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.login_message = 'Войдите сначала, потом будет доступ к странице'

@user.route('/user/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = Bcrypt().generate_password_hash(password=form.password.data).decode('utf-8')
        user = User(name=form.name.data, login=form.login.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Поздравляем, {form.name.data}! Успешно зарегистрированы", "success")
            return redirect('/')
        except Exception as e:
            print(str(e))
    else:
        print('Ошибка регистрации')
    return render_template('user/register.html', form=form)

@user.route('/user/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and Bcrypt().check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"Поздравляем, {form.login.data}! Успешно вошли", "success")
            return redirect(next_page) if next_page else redirect('/')
        else:
            flash(f"Ошибка входа. Проверьте логин и пароль", "danger")
    return render_template('user/login.html', form=form)

@user.route('/user/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect('/')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))