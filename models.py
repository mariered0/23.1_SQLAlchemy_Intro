"""Models for Blogly."""

from unicodedata import name
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Users."""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                           nullable=False)
    image_url = db.Column(db.String(2083), nullable=False, default='https://cdn-icons-png.flaticon.com/512/1246/1246351.png?w=826')
    post = db.relationship('Post', cascade='all, delete-orphan')


class Post(db.Model):
    """Posts."""
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                    nullable=False)
    content = db.Column(db.String(2000),
                    nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete="CASCADE"))
    user = db.relationship('User')

    



    
