from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from server.database import Base

class User(Base):
    """
    Represents an application user.

    Attributes:
        id (int): Primary key for the user.
        username (str): Unique username for login.
        password (str): Hashed password for authentication.
        transactions (list): One-to-many relationship with UserTransaction.
        budgets (list): One-to-many relationship with Budget.
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    transactions = relationship("UserTransaction", back_populates="user", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete-orphan")
