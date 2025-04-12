from sqlalchemy import Column, Integer, String
from database import Base

class Budget(Base):
    __tablename__ = 'budget'