"""Models for Blogly."""

from unicodedata import name
from flask_sqlalchemy import SQLAlchemy

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



    
