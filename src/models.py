import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    # Columnas básicas
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    bio = Column(Text)
    profile_picture = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones con otras tablas
    posts = relationship('Post', back_populates='user',
                         cascade='all, delete-orphan')
    comments = relationship(
        'Comment', back_populates='user', cascade='all, delete-orphan')
    followers = relationship('Follower', foreign_keys='Follower.user_to_id',
                             back_populates='user_to', cascade='all, delete-orphan')
    following = relationship('Follower', foreign_keys='Follower.user_from_id',
                             back_populates='user_from', cascade='all, delete-orphan')
    likes = relationship('Like', back_populates='user',
                         cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "bio": self.bio,
            "profile_picture": self.profile_picture,
            "created_at": self.created_at
        }


class Post(db.Model):
    __tablename__ = 'post'

    # Columnas básicas
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    image_url = Column(String(255), nullable=False)
    caption = Column(Text)
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones con otras tablas
    user = relationship('User', back_populates='posts')
    comments = relationship(
        'Comment', back_populates='post', cascade='all, delete-orphan')
    likes = relationship('Like', back_populates='post',
                         cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Post {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image_url": self.image_url,
            "caption": self.caption,
            "location": self.location,
            "created_at": self.created_at
        }


class Comment(db.Model):
    __tablename__ = 'comment'

    # Columnas básicas
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    comment_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones con otras tablas
    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

    def __repr__(self):
        return f'<Comment {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "comment_text": self.comment_text,
            "created_at": self.created_at
        }


class Follower(db.Model):
    __tablename__ = 'follower'

    # Columnas básicas
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_to_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones con otras tablas
    # user_from = el usuario que SIGUE
    # user_to = el usuario que ES SEGUIDO
    user_from = relationship('User', foreign_keys=[
                             user_from_id], back_populates='following')
    user_to = relationship('User', foreign_keys=[
                           user_to_id], back_populates='followers')

    def __repr__(self):
        return f'<Follower {self.user_from_id} -> {self.user_to_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
            "created_at": self.created_at
        }


class Like(db.Model):
    __tablename__ = 'like'

    # Columnas básicas
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones con otras tablas
    user = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='likes')

    def __repr__(self):
        return f'<Like {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "created_at": self.created_at
        }
