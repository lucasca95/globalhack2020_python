# import os
import datetime
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, DATETIME, Float
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

    def __init__(self, id=0, first_name=None, last_name=None, birthdate=None, email=None, password=None, _type=None, rating=None):
        self.id = id
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
