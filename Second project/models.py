from sqlalchemy import Column, Integer, String
from orm_connection import Base

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True)
    name = Column(String(120), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)
