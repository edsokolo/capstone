from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from flask import url_for
import datetime

from .database import Base, session

post_label_table = Table('post_label_association', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('label_id', Integer, ForeignKey('labels.id'))
)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key = True)
    channel = Column(String, nullable=False)
    social_id = Column(String, nullable=False)
    created_time = Column(DateTime, default=datetime.datetime.now)
    post_url = Column(String, nullable=False)
    img_url = Column(String, nullable=False)

    labels = relationship("Label", secondary="post_label_association",
                            backref="   posts")

    def as_dictionary(self):
        post = {
            "id": self.id,
            "channel": self.channel,
            "social_id":self.social_id,
            "created_time":self.created_time,
            "post_url":self.post_url,
            "img_url":self.img_url,
            "labels": self.labels
        }
        return post

class Label(Base):
    __tablename__ = 'labels'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_time = Column(DateTime, default=datetime.datetime.now)