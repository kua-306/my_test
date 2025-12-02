from sqlalchemy import Column, Integer, String,ForeignKey
from database import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

class Questions(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    answer = Column(String)
    user_id = Column(Integer,ForeignKey('users.id'))

