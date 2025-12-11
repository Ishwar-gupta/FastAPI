from pydantic import BaseModel
from fastapi import FastAPI,Path,HTTPException,Query
from typing import List
import json

app=FastAPI()


@app.get("/")
async def post():
    return {"message":"Patients Management System."}

@app.get("/about")
async def about():
    return {"message":"A fully functional API to manage your patient records"}
@app.get("/details")
def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    
    return data

@app.get("/view")
def view():
    data=load_data()

    return data

@app.get("/patient/{patient_id}") #this is route for accessing details of each patients
async def view_patient(patient_id:str=Path(...,description="ID of the patient in the DB",example="P001")):  #patient_id is the parameter and str is it's annotation
    # load all the patients
    data=load_data()

    if patient_id in data:
        return data[patient_id]
    # return {"Error":"Sorry ,Patients not found!!"}
    raise HTTPException(status_code=404,detail="Patient Not Found")


# problem1
"""
When we execute the patient/patient_id then it isnot declared for searching their details like searching by name or mainly by Id 
like P001,P002...etc

here is the solution for easy access using path() function
# The Path() function in FastAPI is used to provide metadata,validation rules and documentation hints for path parameters in our API endpoints.

Title
Description
Example
ge,gt,le,it (greater than equal or less than equal)
Min_length
Max_length
regex
first step: from fastapi import FastAPI,Path
second step: @app.get("/patient/{patient_id}")
async def view_patient(patient_id:str =Path(...,description='ID of the patient in the DB',example='P001'))  # 3dots means path parameter is required
"""



# problem2
"""
Status Code     Details                         description
200 OK         standard success                a get or post succeeded

404 Not Found   resource doesn't exist         patient id not in db

"""
"""
what if data doesn't exist in db but it returns 200 Ok 
->but it should give 404 not found  error message.

Then it can be handled by HTTPException 
# HTTPException:
it is a special built-in exception in FastAPI used to return custom HTTP error responses when something goes wrong in our API.

Instead of returning a normal JSON or crashing the server.you can gracefully raise an error with:
i)a proper HTTP status code(like 404,400,403,etc.)
ii)a custom error message
iii)(optional)extra headers
"""

# problem3

"""
Query Parameter:
Query parameters are optional key-value pairs appended to the end of a URL,used to pass additional data to the server in an HTTP request.They are typically employed for operations like filtering,sorting,searching,and pagination,without altering the endpoint path itself.

/patients?city=Delhi&sort_by=age

-> The ? marks the start of query parameters
-> Each parameter is a key-value pair:key=value
-> Multiple parameters are separated by &

In this case:
-> city=Delhi is a query parameter for filtering
-> sort_by=age is a query parameter for sorting

# Query function:
Query() is a utility function provided by FastAPI to declare,validate and document query paramters in our API endpoints

It allows us to:
-> set default values
-> Enforce validation rules
-> Add metadata like description , title .

"""

@app.get("/sort")
async def sort_patients(sort_by:str=Query(...,description='Sort on the basis of height,weight or bmi'),order:str=Query('asc',description='sort in ascending or descending order')):
    valid_field=["height","weight","bmi"]

    if sort_by not in valid_field:
        raise HTTPException(status_code=400,detail=f"Invalid field select from {valid_field}")
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Invalid order select between asc and desc')
    
    data=load_data()
    sort_order=True if order=="desc" else False

    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)

    return sorted_data

