"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Creates user instance/record"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.Text)
    posts = db.relationship('Post', backref='user')

# backref should be 'user' because each post would only have one user


class Post(db.Model):
    """Creates post instance/record"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    post_title = db.Column(db.String(50), nullable=False)
    post_content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    post_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    tags = db.relationship('Tag', secondary='posttags', backref='posts')


class Tag(db.Model):
    """Creates a tag"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    name = db.Column(db.String(15), 
                     unique=True)

class PostTag(db.Model):
    """Joins posts and tags together"""

    __tablename__ = "posttags"

    post_id = db.Column(db.Integer, 
                        db.ForeignKey('posts.id'), 
                        primary_key=True)
    tag_id = db.Column(db.Integer, 
                       db.ForeignKey('tags.id'), 
                       primary_key=True)
