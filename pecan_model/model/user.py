from sqlalchemy import Column, Integer, String
from sqlalchemy.ext import declarative


Base = declarative.declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    email = Column(String(64))
