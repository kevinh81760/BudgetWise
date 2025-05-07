from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from server.database import Base

class UserTransaction(Base):
    """
    Represents a financial transaction (income or expense) made by a user.

    Attributes:
        id (int): Primary key for the transaction.
        user_id (int): Foreign key referencing the user.
        category (str): Category of the transaction (e.g., Food, Rent).
        amount (float): Monetary value of the transaction.
        type (str): Either 'income' or 'expen'.
        date_created (datetime): Timestamp of when the transaction was made.
        user (User): Relationship back to the User who made the transaction.
    """
    __tablename__ = "user_transaction"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    category = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String(10), nullable=False)
    date_created = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="transactions")
