from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_CONNECTION_STRING")

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a db session 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the database
Base = declarative_base()

# Function to get the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
