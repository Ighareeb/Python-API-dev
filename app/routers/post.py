# GET ALL POSTS
from app import models, oauth2
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.routers import auth
from app.schemas import CreatePost, Post, TokenData, resPost

router = APIRouter(prefix='/posts/sqlalchemy', tags=['Posts'])
# can use prefic param to simplify code when defining paths
# tag param to group paths together in the FastAPI docs
@router.get('/')
def get_posts(db: Session = Depends(get_db), auth_user: TokenData = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    print(auth_user.user_id)
    return posts

# GET SINGLE POST BY ID
@router.get('/{post_id}', response_model=resPost)
def get_post(post_id: int, db: Session = Depends(get_db), auth_user: TokenData = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f'Post with id {post_id} not found')
    print(auth_user.user_id)
    return post

#CREATE NEW POST
#use post.dict() to convert model to dictonary for when you have a lot of different fields.
#--> then need to use **post.dict() to unpack the dictionary into the function
# eg. new_post = models.Post(**post.dict())
@router.post('/')
# def create_post(db: Session = Depends(get_db)):
#     new_post = models.Post(title='Test Posting new post', content='This is a test post', published=True)
def create_post(post: CreatePost, db: Session = Depends(get_db), auth_user: TokenData = Depends(oauth2.get_current_user)):
    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #similar to RETURNING
    # print(auth_user.user_id)
    print(auth_user.email)
    return new_post
#UPDATE POST
@router.put('/{post_id}')
def update_post(post_id: int, db: Session = Depends(get_db), auth_user: TokenData = Depends(oauth2.get_current_user)):
    updated_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not updated_post:
        raise HTTPException(status_code=404, detail=f'Post with id {post_id} not found')
    updated_post.title = 'Updated Post Title'
    db.commit()
    db.refresh(updated_post)
    print(auth_user.user_id)
    return post_id

# @router.put('/{post_id}')
# alternative if you want client to pass update params. *Note that you need to pass the payload as a dictionary + add pydanctic model for payload
# def update_post(post_id: int, payload: UpdatePostPayload, db: Session = Depends(get_db)):
#     updated_post = db.query(models.Post).filter(models.Post.id == post_id).first()
#     if not updated_post:
#         raise HTTPException(status_code=404, detail=f'Post with id {post_id} not found')
#     updated_post.title = payload.title
#     db.commit()
#     db.refresh(updated_post)
#     return{"data": f'Post with id {post_id} updated'}
# #DELETE POST
@router.delete('/{post_id}')
def delete_post(post_id: int, db: Session = Depends(get_db), auth_user: TokenData = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not deleted_post:
        raise HTTPException(status_code=404, detail=f'Post with id {post_id} not found')
    # deleted_post.delete(synchronize_session=False) #synchronize_session=False to avoid error -?not working properly?
    db.delete(deleted_post)
    db.commit()
    print(auth_user.user_id)
    return post_id