
from pydantic import BaseModel,EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title:str
    content:str
    # published:bool=True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id:int
    # title:str
    # content:str
    # published:bool
    created_at:datetime

    class Config: # this is used to change orm to python dictionary
       from_attributes=True

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    email:EmailStr
    id:int
    created_at:datetime

    class config:
        from_attributes=True


