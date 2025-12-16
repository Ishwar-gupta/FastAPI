from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.params import Body
from typing import List,Optional


app=FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    rating:Optional[int]=None

my_posts=[{"title":"Fruits","content":"Apple,Orange,Litchi,Banana","id":1},{"title":"Vegetable","content":"Cauliflower,Brinjal,Potata,Cabbage","id":2}]

@app.get("/")
def get_posts():
    # return {"message":"This is the  post."}
    return my_posts

@app.post("/create_posts")
def create_post(post:Post):
    print(post.title)
    print(post.content)
    print(post.published)
    print(post.rating)
    print(post.dict())
    return post

@app.post("/new_posts")
def new_post(newPost:dict = Body(...)):
    print(newPost)
    # return {"message":"Successfully created new post."}
    return {"new_post":f"title:{newPost['title']} and content:{newPost['content']}"}

