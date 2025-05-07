from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from server.database import Base

class Budget(Base):
    """
   Represents a user-defined budget goal for a specific category and time range.

    Attributes:
        id (int): Primary key for the budget entry.
        user_id (int): Foreign key referencing the user who owns the budget.
        category (str): Category of the budget (e.g., Food, Rent).
        limit_amount (float): Maximum spending amount allowed.
        start_date (datetime): Start date of the budget period.
        end_date (datetime): End date of the budget period.
        user (User): Relationship back to the User who owns the budget.
    """
    __tablename__ = "budget"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    category = Column(String(50), nullable=False)
    limit_amount = Column(Float, nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    user = relationship("User", back_populates="budgets")
