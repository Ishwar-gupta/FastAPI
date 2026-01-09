from jose import JWTError ,jwt
from datetime import datetime,timedelta
from .import schemas,database,models
from sqlalchemy.orm import Session
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer

from .config import settings

oauth2_shcemas=OAuth2PasswordBearer(tokenUrl='login')
# SECRET_KEY
# Algorithm
# Expiration time

'''for example'''
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_endcode=data.copy()

    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_endcode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_endcode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt 

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str = payload.get("user_id")  # user_id is same as it is in auth.py file which lies in login function of access taken

        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception
    
    return token_data
    
# get_current_user funx calls the verify_access_token 
def get_current_user(token:str=Depends(oauth2_shcemas),db:Session=Depends(database.get_db)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})

    token=verify_access_token(token,credential_exception)
    # return verify_access_token(token,credential_exception)

    user=db.query(models.User).filter(models.User.id==token.id).first()
    if not user:
        raise credentials_exception
    return user
