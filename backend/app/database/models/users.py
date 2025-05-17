from sqlalchemy import Column, String, Integer

from app.database.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)