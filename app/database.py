import os
import sqlalchemy
from sqlalchemy import create_engine #Needs an Engine to connect to DB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

# specify connection string - where DB is located (check psycopg connection similarity in main.py)
# uses specific URL format
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL") 
