from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from server.database import Base

class Budget(Base):
    __tablename__ = "budget"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    category = Column(String(50), nullable=False)
    limit_amount = Column(Float, nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    user = relationship("User", back_populates="budgets")
