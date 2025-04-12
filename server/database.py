from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# create an engine to connect to MySQL
engine = create_engine(
    'mysql+pymysql://root:12345@localhost/budget_app',
    echo=True  # Echo shows SQL statements for debugging (optional)
)

# create a session class
Session = sessionmaker(bind=engine)

# create a base class for models to inherit
Base = declarative_base()
