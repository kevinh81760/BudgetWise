from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    category = Column(String(10), nullable=False)
    amoumt = Column(Float, nullable=False)
    date_created = Column(DateTime, default=datetime)

    user = relationship('User', backref='transaction')

    def __repr__(self):
        return f"<Transaction(user_id={self.user_id}, amount={self.amount}, type='{self.type}')>"
