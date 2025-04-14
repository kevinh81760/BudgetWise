from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from server.database import Base

class UserTransaction(Base):
    __tablename__ = "user_transaction"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    category = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
