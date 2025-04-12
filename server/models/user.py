from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(300), nullable=False)

    def __repr__(self):
        return f"<User(username='{self.username}')>"



