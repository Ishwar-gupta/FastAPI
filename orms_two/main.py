from fastapi import FastAPI
from . import models
# from sqlalchemy.orm import Session
# import psycopg
# from psycopg.rows import dict_row
from .database import engine
from .routers import post,user,auth,vote
# from passlib.context import CryptContext  # passlib package handles password hashes.

from .config import settings 


# pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
# @app.get("/")
# def root():
#     return { "message":"Tables created successfully."}

