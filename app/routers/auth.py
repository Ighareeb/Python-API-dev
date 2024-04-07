from fastapi import HTTPException, Response, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from app.database import get_db
#since we need to interact with DB to verify user
from app.schemas import UserLogin
from app import models, oauth2
from app.utils import verify

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	check_user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
	if not check_user:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials')
	if not verify(user_credentials.password, check_user.password):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials')
	# create token
	access_token = oauth2.create_access_token(data={"user_id": check_user.id}) 
	# where data = what you want to put in token payload
	return {'access_token': access_token, 'token_type': 'bearer'}
	# return {'token': 'example token'} 


# @router.post('/login')
# def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
	# check_user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
# changed to use OAuth2PasswordRequestForm to retrieve user credentials
# note since we are using this util, no longer stored in UserLogin model but in OAuth2PasswordRequestForm class (dict key:v = grant_type, username, password, client_id, client_secret, scope, etc.)
# in this case email will get stored in username key
# !!!IMP so now instead of sending body(raw) as JSON need to send as form data
