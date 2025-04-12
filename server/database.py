from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create an engine to connect to MySQL
# Make sure you have pymysql installed: pip install pymysql
engine = create_engine(
    'mysql+pymysql://root:12345@localhost/budget_app',
    echo=True  # Echo shows SQL statements for debugging (optional)
)

# Create a Session class
Session = sessionmaker(bind=engine)

# Create a Base class for models to inherit
Base = declarative_base()
