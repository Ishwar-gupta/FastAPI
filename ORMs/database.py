
# Object Relational Mapper(ORM)
"""
-> layer of abstraction that sites between the database and fastAPI.
-> We can perform all database operation through traditional python code.No more SQL !
"""
# What can ORMs Do ?
"""
-> Instead of manually defining tables in postgres,we can define our tables as python models.
-> Queries can be made exclusively through python code.No SQL is necessary.
"""
# SQLALCHEMY
"""
-> sqlalchemy is one of the most popular python ORMs.
-> It is used with any other python web frameworks or any python based application.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
# SQLALCHEMY_DATABASE_URL='postgresql://<username>:<password>@<ip-address/hostname>/<database_name'
SQLALCHEMY_DATABASE_URL='postgresql+psycopg://postgres:pgadmin@localhost/fastapi database'

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False, autoflush=False,bind=engine)

# dependencies
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base=declarative_base()
















