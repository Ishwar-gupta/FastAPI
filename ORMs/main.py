from fastapi import FastAPI,HTTPException,status,Depends
from pydantic import BaseModel
from . import models
from sqlalchemy.orm import Session
import psycopg
from psycopg.rows import dict_row
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

@app.get("/")
def root():
    return { "message":"Tables created successfully."}

@app.get("/sqlalchemy")
def test_posts(db: Session= Depends(get_db)):
    return { "status":"success"}


