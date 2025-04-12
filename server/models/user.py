from sqlalchemy import Column, Integer, String, relationship
from database import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(300), nullable=False)
    
    transaction = relationship('Transaction', backref='user', cascade='all, delete-orphan')
    budget = relationship('Budget', backref='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(username='{self.username}')>"



