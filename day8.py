from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from fastapi.params import Body
from random import randrange
from typing import List,Optional
from datetime import datetime

# instance obj
app=FastAPI()

# pydantic model
class Post(BaseModel):
    title:str
    content:str
    published:bool=False
    rating:Optional[int]=None

my_posts=[{
    "title":"Fruits",
    "content":"Apple,Litchi,Banana,Grapes",
    "id":1
},{
    "title":"vegetable",
    "content":"Cauliflower,Cabbage,Brinjal,Potato",
    "id":2
}]

# decorator for details request
@app.get("/")
def get_details():
    return my_posts

# decorator for post request
@app.post("/create_Posts")
def create_posts(post:Post):  # here post is request body data and Post is pydantic model
    post_dict=post.dict()   # here pydantic obj is converted into python dictionary
    post_dict['id']=randrange(0,50)  # generate random id from 0 to 49
    my_posts.append(post_dict)   # appending the new_post into the previous my_post dictionary
    return post_dict    # send the newly created post back to the client

@app.post("/unique_posts")
def unique_post_creation(unique_posts:Post):
    # checking duplicate title if already exists then raise error
    for existing_posts in my_posts:
        if existing_posts['title'].lower() == unique_posts.title.lower():
            return {
                "status":"Failed",
                "Message":"Post with this title already exists"
            }
        
    # converting pydantic obj into python dictionary
    post_dic=unique_posts.dict()

    # server-side values
    post_dic['id']=randrange(1000,9999)
    post_dic['created_at']=datetime.now()
    post_dic['status']="active"

    # saving or appending to the my_posts
    my_posts.append(post_dic)
    return {"status":"Unique posts created successfully","data":post_dic}
    

def find_post(id:int): 

    for pid in my_posts:
        if pid['id']==id:
            print(pid)
            return pid



# Searching posts directly by id 
@app.get("/posts/{id}") #  {id} represents path parameter
# def get_posts(id:int,response:Response):
def get_posts(id:int):
   
    post=find_post(id)
    if not post:
        # response.status_code=404
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'message':f'Post with id {id} was not found.'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} was not found.")
    return {"post_detail":post}
    # print(id)
    # return {"post_details":f"This is the post {id}"}

@app.get("/pts/latest")
def get_latest_posts():
    post=my_posts[len(my_posts)-1]  # this will show top of the stack
    return {"details":post}

