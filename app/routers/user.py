from app import models
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import CreateUser, User
from sqlalchemy.exc import IntegrityError
from typing import List
from app.utils import hash

router = APIRouter()
# CREATE NEW USER
@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    # hash password:
    hased_password = hash(user.password)
    user.password = hased_password
    # new_user = models.User(email=user.email, password=user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail='Email already exists')
    db.refresh(new_user)
    return new_user
# GET ALL USERS
@router.get('/users', response_model=List[User])
def get_posts(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
# GET USER (by id) - see notes
@router.get('/users/{user_id}', response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} not found')
    return user