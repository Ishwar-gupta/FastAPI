# Path Params:
"""
Path parameters are dynamic segments of a URL path used to identify a specific resource.

async def read_item(item_id: int):
Here:

item_id is the parameter

: int is the annotation
→ You are telling FastAPI that item_id must be an integer.

"""


from fastapi import FastAPI
from typing import List

app=FastAPI()

@app.get("/")
async def login():
    return {"message":"Login successfully."}

