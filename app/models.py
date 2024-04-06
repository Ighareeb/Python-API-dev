from time import timezone
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text
from .database import Base

# Every model defined represents a table in the DB
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 
    
class User(Base):
    __tablename__ = 'users'    
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 


# note for ID - not specifying autoincrement=True/serial data type since RBDs automatically treat primary_key columns as autoincrementing.









