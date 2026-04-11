from flask import Flask
from .routes.user import user, login_manager
from .routes.post import post
from .routes.main import main
from .extentions import db
import os
from sqlalchemy import inspect

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///petproject.db'
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_ECHO'] = True

    app.register_blueprint(user)
    app.register_blueprint(post)
    app.register_blueprint(main)

    login_manager.init_app(app)


    db.init_app(app)
    with app.app_context():
        db.create_all()

    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print("Таблицы в базе данных:", tables)

    return app
