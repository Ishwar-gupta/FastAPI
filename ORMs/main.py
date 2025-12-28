from fastapi import FastAPI,HTTPException,Response,status,Depends
from pydantic import BaseModel
from . import models
from sqlalchemy.orm import Session
import psycopg
from psycopg.rows import dict_row
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)

app=FastAPI()
class Post(BaseModel):
    title:str
    content:str
    published:bool=True

@app.get("/")
def root():
    return { "message":"Tables created successfully."}


@app.get("/sqlalchemy")
def test_posts(db: Session= Depends(get_db)):
    posts=db.query(models.Post).all()
    return { "status":posts}

# searching posts with id
@app.get("/posts/{id}")
def get_post(id:int,db:Session=Depends(get_db)):
   post= db.query(models.Post).filter(models.Post.id==id).first()
   print(post)
   
   if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found.")
   return {"post_detail":post}


# creating post using orms model
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post,db:Session=Depends(get_db)):
    new_post=models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # returning back
    return {"data":new_post}

# deleting posts
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int , db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id)

    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} doesn't exists.")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# updating post
@app.put("/posts/{id}")
def update_post(id:int,updated_post:Post, db:Session=Depends(get_db)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    if post == None: # if post doesn't exists
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} doesn't exists.")
    
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()

    return {"data": post_query.first()} 
