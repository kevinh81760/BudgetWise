from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Budget(Base):
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    category = Column(String(50), nullable=False)
    limit_amount = Column(Float, nullable=False)
    start_date = Column(DateTime, default=datetime)
    end_date = Column(DateTime)