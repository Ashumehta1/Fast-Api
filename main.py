#uvicorn main:app --reload
from fastapi import FastAPI,Path,HTTPException,Query
import json
from pydantic import BaseModel,Field
#to add description in pydantic need to import Annotated from typing
from typing import Annotated,List

app=FastAPI()

#pydantic
class patient(BaseModel):
    id:Annotated[str,Field(...,description="Id of patient", examples=["P001"])]
    name:str
    age:int
    gender:str
    blood_group:str
    contact:str
    address:str
    medical_history:List[str]
    allergies:List[str]
    height:float
    weight:float
    bmi:float

#load data
def load_data():
    with open("patient.json" , "r") as f:
        data=json.load(f)
    return data

@app.get("/")
def patient_page():
    return {"Wlcome to patient page"}

@app.get("/about")
def about():
    return {"It is API for patient management"}

@app.get("/view")
def view():
    data=load_data()
    return data

# path parameter
@app.get("/patient_view/{patient_id}")
def patient_view(patient_id:str = Path(...,description='It is ID of patient',example='P001')):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    #return {"error":"patient not found"}
    raise HTTPException(status_code=404,detail="patient not found")

# Query parameter
@app.get("/sort")
def sort_patients(sort_by:str = Query(...,description="sort on the basis of height or age"),
                  order_by:str=Query('asc',description="sort in asc or desc else defoult sort by asc")):
    valid_field=["height","age"]
    if sort_by not in valid_field:
        raise HTTPException(status_code=400,detail=f"invalid field selected , select from {valid_field}")
    if order_by not in ["asc","desc"]:
        raise HTTPException(status_code=400, detail="invalid order selected, select from asc or desc, default asc")
    data=load_data()
    sort_order=True if order_by =="desc" else False
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
    return sorted_data

