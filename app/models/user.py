from datetime import datetime
from flask_login import UserMixin
from ..extentions import db
from ..models.post import Post


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    posts = db.relationship(Post, backref='author')
    status = db.Column(db.String(50), default="user")
    name = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)