import email
import json
from multiprocessing import synchronize
import os
import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
import psycopg
# from pydantic import BaseModel, Json - moved schema to separate file
from app import models
from sqlalchemy.orm import Session

from app.models import Post, User
from app.database import engine, get_db
from sqlalchemy.exc import IntegrityError
from app.schemas import CreatePost, Post, CreateUser, User, resPost
from app.utils import hash
from random import randrange
from dotenv import load_dotenv

from .routers import post, user, auth



# from httpx import get, post (httpx library Python -HTTP client library, provides sync and async APIs)

load_dotenv()
DB_HOST=os.getenv('DB_HOST')
DB_NAME=os.getenv('DB_NAME')
DB_USER=os.getenv('DB_USER')
DB_PASS=os.getenv('DB_PASS')


# Create models defined in model.py  
models.Base.metadata.create_all(bind=engine)
# create dependency for route handlers (func to create db Session to interact with DB)
# Session starts when request is received and ends when response is sent


app = FastAPI()



# -------------------------------------------------------------------
# Connect to PostgreSQL DB using psycopg
# while loop and try-except block to handle connection error
while True:
    try:
        conn = psycopg.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
        cursor = conn.cursor()
        print('Connected to PostgreSQL DB')
        break
    except Exception as e:
        print(f"Error: {e} - Error connecting to PostgreSQL DB")
        time.sleep(2)
        
# --------------------------USING SQL Alechemy (moved to separate files-----------------------------------------  
# # GET ALL POSTS
# @app.get('/posts/sqlalchemy/')
# def get_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts

# # GET SINGLE POST BY ID
# @app.get('/posts/sqlalchemy/{post_id}', response_model=resPost)
# def get_post(post_id: int, db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == post_id).first()
#     if not post:
#         raise HTTPException(status_code=404, detail=f'Post with id {post_id} not found')
#     return post

# #CREATE NEW POST
# #use post.dict() to convert model to dictonary for when you have a lot of different fields.
# #--> then need to use **post.dict() to unpack the dictionary into the function
# # eg. new_post = models.Post(**post.dict())
# @app.post('/posts/sqlalchemy/')
# # def create_post(db: Session = Depends(get_db)):
# #     new_post = models.Post(title='Test Posting new post', content='This is a test post', published=True)
# def create_post(post: CreatePost, db: Session = Depends(get_db)):
#     new_post = models.Post(title=post.title, content=post.content, published=post.published)
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post) #similar to RETURNING
#     return new_post
# #UPDATE POST
# @app.put('/posts/sqlalchemy/{post_id}')
# def update_post(post_id: int, db: Session = Depends(get_db)):
#     updated_post = db.query(models.Post).filter(models.Post.id == post_id).first()
#     if not updated_post:
#         raise HTTPException(status_code=404, detail=f'Post with id {post_id} not found')
#     updated_post.title = 'Updated Post Title'
#     db.commit()
#     db.refresh(updated_post)
#     return post_id
# @app.put('/posts/sqlalchemy/{post_id}')

# # alternative if you want client to pass update params. *Note that you need to pass the payload as a dictionary + add pydanctic model for payload
# # def update_post(post_id: int, payload: UpdatePostPayload, db: Session = Depends(get_db)):
# #     updated_post = db.query(models.Post).filter(models.Post.id == post_id).first()
# #     if not updated_post:
# #         raise HTTPException(status_code=404, detail=f'Post with id {post_id} not found')
# #     updated_post.title = payload.title
# #     db.commit()
# #     db.refresh(updated_post)
# #     return{"data": f'Post with id {post_id} updated'}
# # #DELETE POST
# @app.delete('/posts/sqlalchemy/{post_id}')
# def delete_post(post_id: int, db: Session = Depends(get_db)):
#     deleted_post = db.query(models.Post).filter(models.Post.id == post_id).first()
#     if not deleted_post:
#         raise HTTPException(status_code=404, detail=f'Post with id {post_id} not found')
#     # deleted_post.delete(synchronize_session=False) #synchronize_session=False to avoid error -?not working properly?
#     db.delete(deleted_post)
#     db.commit()
#     return post_id
# ----------------USERS---------------------------------------------
# CREATE NEW USER
# @app.post('/users', status_code=status.HTTP_201_CREATED, response_model=User)
# def create_user(user: CreateUser, db: Session = Depends(get_db)):
#     # hash password:
#     hased_password = hash(user.password)
#     user.password = hased_password
#     # new_user = models.User(email=user.email, password=user.password)
#     new_user = models.User(**user.model_dump())
#     db.add(new_user)
#     try:
#         db.commit()
#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(status_code=400, detail='Email already exists')
#     db.refresh(new_user)
#     return new_user
# # GET ALL USERS
# @app.get('/users', response_model=List[User])
# def get_posts(db: Session = Depends(get_db)):
#     users = db.query(models.User).all()
#     return users
# # GET USER (by id) - see notes
# @app.get('/users/{user_id}', response_model=User)
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} not found')
#     return user
# -------------------------------------------------------------------
# Using SQLAlchemy with routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
# -------------------------------------------------------------------

# my posts array
# my_posts = [
#     {
#         "post": {"title": "Post 1", "content": " Content 1"},
#         "published": True,
#         "rating": 5,
#         "postId": 1,
#     },
# ]


# def find_post_by_id(post_id: int):
#     for p in my_posts:
#         if p["postId"] == post_id:
#             return p


# -------------------------------------------------------------------
# # 'path operation' is a function that is defined in a FastAPI application (i.e. route handler)
# @app.get(
#     "/"
# )  # 'decorator' for the function to define api HTTP method and path that fastAPI app should use
# def root_hello_world():
#     return {
#         "message": "Hello World"
#     }  # FastAPI returns a dictionary that will be converted to JSON and sent to the client
# -------------------------------------------------------------------
# GET - ALL POSTS
# @app.get("/posts")
# def get_posts():
#     # return {"message": "Get all Posts", "data": "All Posts"}
#     # return {"data": my_posts}
#     cursor.execute("SELECT * FROM posts")
#     posts = cursor.fetchall()
#     print(posts)
#     return posts


# # GET latest post (order matters since route would be consider a match with GET single post route)
# @app.get("/posts/latest")
# def get_latest_post():
#     # post = my_posts[len(my_posts) - 1]
#     # return {"data": post}
#     cursor.execute("SELECT * FROM posts ORDER BY post_id DESC LIMIT 1")
#     latest_post = cursor.fetchone() 
#     print(latest_post)
#     return latest_post


# # GET - SINGLE POST BY ID
# @app.get("/posts/{post_id}")
# # def get_post(post_id: int, response: Response):
# def get_post(post_id: int):
#     # post = find_post_by_id(post_id)
#     cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,) )
#     post = cursor.fetchone()
#     if not post:
#         # 1. hard-coded response
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message": f"Post with id {post_id} not found"} 
#         # 2. using HTTPException from fastapi
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id {post_id} not found",
#         )
#     return post


# # -------------------------------------------------------------------
# # POST - CREATE NEW POST
# # @app.post("/posts")
# # def create_post(payload: dict = Body(...)):
# #     print(payload)
# #     return {
# #         "new_post": f"title: {payload['post']['title']} content: {payload['post']['content']}"
# #         # payload['post'] since title and content are nested in post key
# #     }
# # similar as above but using Pydantic
# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(payload: Post):
#     # !!!if you use string interpolation then you are vulnerable to SQL injection
#     cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (payload.title, payload.content, payload.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return new_post
#     # post_dict = payload.model_dump()
#     # post_dict["postId"] = randrange(0, 1000000000000)
#     # print(payload)
#     # print(post_dict)  # model_dump since dict() is deprecated
#     # my_posts.append(post_dict)
#     # return {
#     #     "new_post": f"title: {payload.post.title} content: {payload.post.content} published: {payload.published} rating: {payload.rating}"
#     # }


# # -------------------------------------------------------------------
# # UPDATE - UPDATE POST
# @app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
# def update_post(post_id: int, payload: Post):
#     cursor.execute("""UPDATE public.posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (payload.title, payload.content, payload.published, post_id))
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if not updated_post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id {post_id} not found",
#         )
#     return post_id
#     # post = find_post_by_id(post_id)
#     # if post:
#     #     for i, p in enumerate(my_posts):
#     #         updated_post = payload.model_dump()
#     #         updated_post["postId"] = post_id
#     #         my_posts[i] = updated_post
#     #         return {"message": f"Post with id {post_id} updated", "data": post}


# # -------------------------------------------------------------------
# # DELETE - DELETE POST
# @app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(post_id: int):
#     # post = find_post_by_id(post_id)
#     # cursor.execute("SELECT * FROM posts where id = %s ", (post_id,))
#     cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (post_id,))
#     deleted_post = cursor.fetchone()
#     print(deleted_post)
#     conn.commit()
#     if not deleted_post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id {post_id} not found",
#         )
#     # my_posts.remove(post)
#     # return Response(status_code=status.HTTP_204_NO_CONTENT)
#     return post_id

