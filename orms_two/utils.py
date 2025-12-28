from passlib.context import CryptContext  # passlib package handles password hashes.

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash(password:str)->str:
    return pwd_context.hash(password)