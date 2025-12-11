# This file include all the details of fastAPI from scratch

# from fastapi import FastAPI

# app=FastAPI()

# @app.get("/")
# async def root():
#     return {"message":"Hello World"}

"""

create a path operation¶
Path¶
"Path" here refers to the last part of the URL starting from the first /.

So, in a URL like:


https://example.com/items/foo
...the path would be:


/items/foo
Info

A "path" is also commonly called an "endpoint" or a "route".

While building an API, the "path" is the main way to separate "concerns" and "resources".

Operation¶
"Operation" here refers to one of the HTTP "methods".

One of:

POST
GET
PUT
DELETE
...and the more exotic ones:

OPTIONS
HEAD
PATCH
TRACE
In the HTTP protocol, you can communicate to each path using one (or more) of these "methods".

When building APIs, you normally use these specific HTTP methods to perform a specific action.

Normally you use:

POST: to create data.
GET: to read data.
PUT: to update data.
DELETE: to delete data.
So, in OpenAPI, each of the HTTP methods is called an "operation".

We are going to call them "operations" too.

Define a path operation decorator¶

Python 3.8+

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

The @app.get("/") tells FastAPI that the function right below is in charge of handling requests that go to:

the path /
using a get operation
@decorator Info

That @something syntax in Python is called a "decorator".

You put it on top of a function. Like a pretty decorative hat (I guess that's where the term came from).

A "decorator" takes the function below and does something with it.

In our case, this decorator tells FastAPI that the function below corresponds to the path / with an operation get.

It is the "path operation decorator".

You can also use the other operations:

@app.post()
@app.put()
@app.delete()
And the more exotic ones:

@app.options()
@app.head()
@app.patch()
@app.trace()
"""


from fastapi import FastAPI

app=FastAPI()

@app.get("/")  # @app is the decorator where get is method and "/"is the path
async def login_user(): # login_user is the function name
    return {"First_Name":"Siddheshwar",
            "Last_Name":"Gupta",
            "Message":"Welcome to the  api documentation!!!!",
            "message2":"Hello World"}
@app.get("/posts")
def get_post():
    return {"data":"This is your posts"}

# If we declare two get("/") method then upper one run only & other are dominated
@app.get("/")
async def sign_up():
    return {"data":"this is your sign_up page"}

