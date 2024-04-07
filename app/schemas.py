from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.database import Base

# REQUEST MODELS
class Post(BaseModel):
    # post: PostContent  
    title: str
    content: str
    published: bool  
    # rating: Optional[int] = None

# EXAMPLE by using separate classes/models for different CRUD, able to define different rules. eg user can't update certain fields
class CreatePost(Post):
    pass  
# # pass keyword acts as placeholder. Since CreatePost is extending Post, it will inherit all the fields from Post, so pass just means no other changes to 'Post' BaseModel
    
# class UpdatePost(Post):
# 	pass
# --------------------------------------------------------
# RESPONSE MODELS -note can use a base model to inherit from as before
# need to add 
# --> will only return defined/specific fields; or can be used to modify/validate data type to return (in request when we did return we got id and created_at as well even though not defined in the model)
class resPost(BaseModel):
    title: str
    content: str
    published: bool 
    # created_at: datetime
    class Config:
        from_attributes = True 
# need to add Config class because Pydantic models are not the same as SQLAlchemy models. They use dictionsaries to store data, while SQLAlchemy uses objects. So need to tell Pydantic to treat the SQLAlchemy model as a dictionary.


# USER MODELS

class CreateUser(BaseModel):
    email: EmailStr
    password: str
    
class User(BaseModel):
    id: int
    email: str
    created_at: datetime
    # don't want to return password!
    class Config:
        from_attributes = True

# AUTHENTICATION SCHEMA MODEL
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Token schema model
class Token(BaseModel):
    access_token: str
    token_type: str
# define schema for Token payload data
class TokenData(BaseModel):
    user_id: Optional[int] = None

# auth.py
# access_token = oauth2.create_access_token(data={"user_id": check_user.id}) 
# {'access_token': access_token, 'token_type': 'bearer'}