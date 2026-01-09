
from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title:str
    content:str
    # published:bool=True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    email:EmailStr
    id:int
    created_at:datetime

    class config:
        from_attributes=True

class Post(PostBase):
    id:int
    # title:str
    # content:str
    published:bool=True
    created_at:datetime
    owner_id:int
    owner:UserOut

    class Config: # this is used to change orm to python dictionary
       from_attributes=True

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]=None  # i have changed from str to int 

class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)
