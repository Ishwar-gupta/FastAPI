from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel
from typing import List,Optional
from fastapi.params import Body
from random import randrange

app=FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool=None
    rating:Optional[float]=None


my_posts=[{
    "title":"Fruits",
    "content":"Apple,Litchi",
    "id":1
},{
    "title":"Vegetable",
    "content":"Cauliflower,Cabbage",
    "id":2
},{
    "title":"Books",
    "content":"Python",
    "id":3
}]

def find_index_post(id:int):
    for i ,p in enumerate(my_posts):
        if p['id']==id:
            return i

@app.get("/")
def get_posts():
    return my_posts

@app.post("/Create_posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    dict_form=post.model_dump()
    dict_form['id']=randrange(10,100)
    my_posts.append(dict_form)
    return dict_form

@app.put("/update_posts/{id}")
def update_post(id:int,post:Post):
    index=find_index_post(id)
    
    if index ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post wtih id {id} doesn't exists")
    dict_form=post.model_dump()
    dict_form['id']=id
    my_posts[index]=dict_form
    return {"data":dict_form}