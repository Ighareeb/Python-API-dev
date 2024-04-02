import json
from time import time
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel, Json
from random import randrange
import psycopg

app = FastAPI()


# Validation --> Pydantic Schema models that extends BaseModel
class PostContent(BaseModel):
    title: str
    content: str


class Post(BaseModel):
    post: PostContent  
    published: bool = True
    rating: Optional[int] = None
# -------------------------------------------------------------------
# Connect to PostgreSQL DB using psycopg
# while loop and try-except block to handle connection error
while True:
    try:
        conn = psycopg.connect(host='localhost', dbname='fastapi_tutorial', user='postgres', password='ig1955')
        cursor = conn.cursor()
        print('Connected to PostgreSQL DB')
        break
    except Exception as e:
        print(f"Error: {e} - Error connecting to PostgreSQL DB")
        time.sleep(2)
    

# -------------------------------------------------------------------
# my posts array
my_posts = [
    {
        "post": {"title": "Post 1", "content": "Content 1"},
        "published": True,
        "rating": 5,
        "postId": 1,
    },
]


def find_post_by_id(post_id: int):
    for p in my_posts:
        if p["postId"] == post_id:
            return p


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
@app.get("/posts")
def get_posts():
    # return {"message": "Get all Posts", "data": "All Posts"}
    return {"data": my_posts}


# GET latest post (order matters since route would be consider a match with GET single post route)
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"data": post}


# GET - SINGLE POST
@app.get("/posts/{post_id}")
def get_post(post_id: int, response: Response):
    post = find_post_by_id(post_id)
    if not post:
        # 1. hard-coded response
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {post_id} not found"}
        # 2. using HTTPException from fastapi
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )
    return {"data": post}


# -------------------------------------------------------------------
# POST - CREATE NEW POST
# @app.post("/posts")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {
#         "new_post": f"title: {payload['post']['title']} content: {payload['post']['content']}"
#         # payload['post'] since title and content are nested in post key
#     }
# similar as above but using Pydantic
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    post_dict = payload.model_dump()
    post_dict["postId"] = randrange(0, 1000000000000)
    print(payload)
    print(post_dict)  # model_dump since dict() is deprecated
    my_posts.append(post_dict)
    # return {
    #     "new_post": f"title: {payload.post.title} content: {payload.post.content} published: {payload.published} rating: {payload.rating}"
    # }
    return {"data": post_dict}


# -------------------------------------------------------------------
# UPDATE - UPDATE POST
@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
def update_post(post_id: int, payload: Post):
    post = find_post_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )
    if post:
        for i, p in enumerate(my_posts):
            updated_post = payload.model_dump()
            updated_post["postId"] = post_id
            my_posts[i] = updated_post
            return {"message": f"Post with id {post_id} updated", "data": post}


# -------------------------------------------------------------------
# DELETE - DELETE POST
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    post = find_post_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )
    my_posts.remove(post)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    return {"message": f"Post with id {post_id} deleted"}