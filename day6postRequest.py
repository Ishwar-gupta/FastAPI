from fastapi import FastAPI,Path,HTTPException,Query
from pydantic import BaseModel,computed_field,Field
from fastapi.responses import JSONResponse
from typing import List,Annotated,Literal
import json

app=FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(..., description="ID of the patient",example='P001')]
    name:Annotated[str,Field(..., description='Name of the patient')]
    city:Annotated[str,Field(..., description='city where the patient is living')]
    age:Annotated[int,Field(..., gt=0 ,lt=120,description='Age of the patient')]
    gender:Annotated[Literal['Male','Female','Others'],Field(..., description='Gender of the patient')]
    height:Annotated[float,Field(..., gt=0,description='Height of the  patient in mtrs')]
    weight:Annotated[float,Field(..., gt=0 , description='Weight of the patient in kgs')]
    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi > 30:
            return "Overweight"
        else :
            return 'Obese'
       

def load_data():
    try:
        with open('patients.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)


@app.post("/create")
def create_patient(patient:Patient):  #patient is pydantic object

    # load existing data
    data=load_data()

    # check if the patient is already exists
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists')
    

    # new patient added to the database
    # here .model_dump() is used to change the  pydantic obj into python dictionary
    data[patient.id]=patient.model_dump(exclude=['id'])
    
    # saving int the json file
    save_data(data)

    return JSONResponse(status_code=201,content={"message":"Patient created successfully"})