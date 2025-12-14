"""
from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()


@app.get("/")
async def getUser():
    return {"message":"Hello World"}
 @app.get("/data")
def insert_patient_data(name:str,age:int):
   if type(name)==str and type(age)==int:
       return {name,age}
   else:
       raise TypeError("Incorrect data type")
   

insert_patient_data("sid",25)
"""

'''
# but this method is not scalable
def insert_patient_data(name:str,age:int):
   if type(name)==str and type(age)==int:
        if age < 0 :
            raise ValueError("Age can't be negative.")
        else:
            print(name)
            print(age)
            print("Inserting the data into database.")

   else:
       raise TypeError("Incorrect data type")
insert_patient_data("sid",23)

def update_patient_data(name:str,age:int):
    if type(name)== str and type(age)== int:
        if age < 0 :
            raise ValueError("Age cant't be negative.")
        else:
            print(name)
            print(age)
            print("updating the data into database.")
    else:
        raise TypeError("Incorrect Data type.")
                        
'''

# Pydantic follows 3 step i.e
"""
1. Define Pydantic model that  represents the ideal schema of the data.
 -> This includes the expected fields , their types , and any validation constraints(e.g., gt=0 for positive numbers.)
2.Instantiate the model with raw input data(usually a dictionary or JSON-like structure).
 -> Pydantic will automatically validate the data and coerce it into the correct Python types(if possible).
  ->If the data doesn't meet the model's requirements,Pydantic raises a validatoionError.
3. Pass the validated model object to functions or use it throughout your codebase.
 -> This ensures that every part of your program works with clean ,type-safe and logically valid data.

"""

from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):  #it shows pydantic model
    # ideal schema defining
    # name:str=Field(max_length=50)
    name:Annotated[str,Field(max_length=50,title='Name of the patient',description='Give the name of the patient in less than 50 chars',example=['sid','rajiv','sameep'])]  # this is all called meta-data
    email:EmailStr
    age:int=Field(gt=0,lt=120)  # greater than 0 and lessthan 120
    linkedin_url:AnyUrl
    weight:float=Field(gt=0)  # meand weight constraints should be greater than 0  i.e doesn't take neg num
    # married:bool=False
    married:Annotated[bool,Field(default=None,description='Is the patient married or not')]
    # allergies:Optional[List[str]] =None  # Optional is used for making data optional if patient doesn't have this prblm
    allergies:Annotated[List[str],Field(default=None,max_length=5)]
    contact_details:dict[str,str]

def insert_patient_data(patient:Patient):
   print(patient.name)
   print(patient.email)
   print(patient.age)
   print(patient.weight)
   print(patient.married)
   print(patient.allergies)
   print(patient.contact_details)
   print(patient.linkedin_url)

   print("Inserting data.")

def update_patient_data(patient:Patient):
   print(patient.name)
   print(patient.age)
   print("Updated data.")
# if @ is left mistakely then it gives error
patient_info={'name':'Siddheshwar',"email":"siddhu@gmail.com","age":22,"linkedin_url":"https://linkedin.com","weight":75.4,'contact_details':{"contact":"9742913490"}}  # if "age":"thirty" then it gives error due to type error

patient1=Patient(**patient_info)  # ** helps to unpack the dictionary 
insert_patient_data(patient1)
# update_patient_data(patient1)
    
