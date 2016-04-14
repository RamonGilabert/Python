from sqlalchemy import Column, Integer, String
from orm_connection import Base

class User(Base):
    __tablename__ = 'ORM_Users'
    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True)
    name = Column(String(120))
    email = Column(String(120))
    password = Column(String(120))

    def __init__(self, username=None, name=None, email=None, password=None):
        self.username = username
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)
