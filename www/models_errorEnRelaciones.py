# import os
import datetime
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, DATETIME, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):
    __tablename__ = 'appuser'
    id = Column(Integer, primary_key=True)
    first_name = Column('first_name', String(20))
    last_name = Column('last_name', String(20))
    birthdate = Column('birthdate', DATETIME)
    email = Column('email', String(30))
    password = Column('password', String(100))
    _type = Column('type', String(1))
    rating = Column('rating', Float)
    
    # Relation with Petition
    petitions_helped = relationship('Petition', back_populates="helped")
    petitions_collaborator = relationship('Petition', back_populates="collaborator")

    # Relation with Review
    reviews = relationship("Review", back_populates="user")
    


    def __init__(self, first_name=None, last_name=None, birthdate=None, email=None, password=None, _type=None, rating=None):
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.email = email
        self.password = password
        self._type = _type
        self.rating = rating

    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'  : self.id,
           'first_name': self.first_name,
           'last_name': self.last_name,
           'birthdate': self.birthdate,
           'email': self.email,
           'type': self._type,
           'rating': self.rating
        }


class Petition(Base):
    __tablename__ = 'petition'
    id = Column(Integer, primary_key=True)
    day = Column('day', DATETIME)
    hour = Column('hour', DATETIME)
    gift = Column('gift', String(100))

    # Relation with User
    helped_id = Column(Integer, ForeignKey('appuser.id'))
    helped = relationship("User", back_populates="petitions_helped")
    collaborator_id = Column(Integer, ForeignKey('appuser.id'))
    collaborator = relationship("User", back_populates="petitions_collaborator")

    # Relation with Review
    reviews = relationship("Review", back_populates="petition")

    def __init__(self, day=None, hour=None, gift=None):
        self.day = day
        self.hour = hour
        self.gift = gift

    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'  : self.id,
           'day': self.day,
           'hour': self.hour,
           'gift': self.gift
        }


class Review(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    comment = Column('comment', String(140))
    rating = Column('rating', Float)

    # Relation User
    user_id = Column(Integer, ForeignKey('appuser.id'))
    user = relationship("User", back_populates="reviews")

    # Relation Petition
    petition_id = Column(Integer, ForeignKey('petition.id'))
    petition = relationship("Petition", back_populates="reviews")


    def __init__(self, comment=None, rating=None, gift=None):
        self.comment = comment
        self.rating = rating

    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'  : self.id,
           'comment': self.comment,
           'rating': self.rating
        }
