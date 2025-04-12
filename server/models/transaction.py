from sqlalchemy import Column, Integer, String
from database import Base

class Transaction(Base):
    __tablename__ = 'transaction'