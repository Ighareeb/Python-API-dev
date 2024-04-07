from time import timezone
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text
from .database import Base
from sqlalchemy.orm import relationship

# Every model defined represents a table in the DB
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    # user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    # user = relationship('User', back_populates='posts')
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 
    
class User(Base):
    __tablename__ = 'users'    
    
    id = Column(Integer, primary_key=True, nullable=False)
    # posts = relationship('Post', back_populates='user', cascade='all, delete-orphan')
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 


# note for ID - not specifying autoincrement=True/serial data type since RBDs automatically treat primary_key columns as autoincrementing.

# cascade option means if user is deleted, all posts by that user will be deleted as well








