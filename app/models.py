from sqlalchemy import Boolean, Column, Integer, String
from .database import Base

# Every model defined represents a table in the DB
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    
    











