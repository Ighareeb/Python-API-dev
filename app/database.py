import os
from sqlalchemy import create_engine #Needs an Engine to connect to DB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

# SET UP SQLAlchemy connection to DB + Setup session
# specify connection string - where DB is located (check psycopg connection similarity in main.py)
# uses specific URL format
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL") 

engine = create_engine(SQLALCHEMY_DATABASE_URL) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() #define Base class that my defined models will extend

def get_db():
    db = SessionLocal()
    try:
        yield db # yield keyword vs return --> makes it a generator function
    finally:
        db.close()