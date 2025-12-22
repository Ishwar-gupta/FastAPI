from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time

app=FastAPI()

# pydantic model
class Post(BaseModel):
    title:str
    content:str
    published:bool=True

while True:
    try:
        conn=psycopg.connect(host='localhost', dbname='fastapi database',user='postgres',password='pgadmin',row_factory=dict_row)
        cursor=conn.cursor()
        print("Database connection was successful.")
        break
    except Exception as error:
        print("Connection to the database is failed")
        print("Error:",error)
        time.sleep(2) # if any wrong user or password




# ********************* Fetching data  ***************************************************************

@app.get("/posts")
def get_posts():
    posts=cursor.execute(""" SELECT * FROM posts """)
    posts=cursor.fetchall()
    return posts

# *******************  Create-Posts  ***************************************************************

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
   
    # cursor.execute(f" INSERT INTO posts (title,content,published) VALUES ({post.title},{post.content},{post.published})")
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s , %s , %s) RETURNING *; """,
                   (post.title,post.content,post.published))
    new_post=cursor.fetchone()
    conn.commit()  # it commit in the database
    return new_post
# *********** Searching post with id ****************************************************************
# searching post by its id
@app.get("/posts/{id}")
def get_post(id:int):
    # selecting all the data of table 
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(id,))
    post=cursor.fetchone()
    #  validation:if post with specific id wasn't exists
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} wasn't found")
    
    # returning post details
    return {"post_detail":post}
# ***************Updating posts *********************************************************

# updation in CRUD operation in database
@app.put("/update_post/{id}")
def update_post(id:int,post:Post):
    # updating posts with help of id
    cursor.execute(""" UPDATE posts SET title= %s ,content=%s,published=%s WHERE id =%s RETURNING * """,(post.title , post.content , post.published,str(id)))
    updated_post=cursor.fetchone()  
    conn.commit()  # updating into database also

    #  eixistation validation if such post with specific id exists or not
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} doesn't exists !!")
    
    # retruning the updated post
    return {"data":updated_post}

# *******************  Deleting post**************************************************************

# deleting posts by it's id
@app.delete("/delete_posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
   cursor.execute(""" DELETE FROM posts WHERE id = %s returning *; """,(id,))
   deleted_post=cursor.fetchone()
   conn.commit()
    
   if deleted_post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post wtih id {id} doesn't exists")

