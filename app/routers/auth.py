from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session 
from app.database import get_db
#since we need to interact with DB to verify user
from app.schemas import UserLogin
from app import models
from app.utils import verify


router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
	check_user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
	if not check_user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')
	if not verify(user_credentials.password, check_user.password):
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')
	# create token
	return {'token': 'example token'}