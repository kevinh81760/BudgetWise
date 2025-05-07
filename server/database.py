from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Create the engine to connect to the SQLite database
engine = create_engine("sqlite:///budgetwise.db", echo=True)

# 2. Declare a base class for models to inherit from
Base = declarative_base()

# 3. Create a session factory bound to the engine
Session = sessionmaker(bind=engine)








