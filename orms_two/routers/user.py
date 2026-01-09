from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from .. database import get_db

router=APIRouter(
  prefix="/users",  # we don't need to declare "/posts" in every decorators simply
  tags=['Users']   # it differentiate the Posts and User documentation in Swagger UI   
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session= Depends(get_db)):
    # hash the password->user.password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password

    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} doesn't exists.")
    return user
