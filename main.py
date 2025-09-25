#uvicorn main:app --reload
from fastapi import FastAPI,Path,HTTPException,Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
#to add description in pydantic need to import Annotated from typing
from typing import Annotated,List,Literal

app=FastAPI()

#pydantic
class patient(BaseModel):
    id:Annotated[str,Field(...,description="Id of patient", examples=["P001"])]
    name:Annotated[str,Field(...,description="Name of patient", examples=["Ashish"])]
    age:Annotated[int,Field(...,description="Age of patient",ge=0,lt=150)]
    gender:Annotated[Literal["male","female","others"],Field(...,description="gender of the patient")]
    blood_group:Annotated[str,Field(..., description="bload group of patient", examples=["A+"])]
    contact:Annotated[str,Field(description="contact details")]
    address:Annotated[str,Field(description="Address of patient")]
    medical_history:Annotated[List[str],Field(description="any medical record if any")]
    allergies:Annotated[List[str],Field(description="any type of allergies")]
    height:Annotated[float,Field(...,description="height of the patient in mtrs", ge=0,examples=[1.4])]
    weight:Annotated[float,Field(...,description="weight of patient in kg",ge=0,examples=[80.5])]
    

@computed_field
@property
def bmi(self) -> float:
    """Automatically calculate BMI from height & weight"""
    bmi=self.weight/(self.height**2)
    return round(bmi,2)

@computed_field
@property
def vedic(self) -> str:
    """BMI category based on WHO standards"""
    if self.bmi < 18.5:
        return "underweight"
    elif self.bmi < 25:
        return "normal"
    elif self.bmi < 30:
        return "overweight"
    else:
        return "obese"

#load data
def load_data():
    with open("patient.json" , "r") as f:
        data=json.load(f)
    return data

#save data
def save_data(data):
    with open("patient.json","w") as f:
        json.dump(data,f)

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

@app.post("/create")
def patient_create(patient:patient):
    #get data in patient variable and check and validate by patient pydantic
    #load data
    data=load_data()
    #chech patient exist or not
    if patient.id in data:
        raise HTTPException(status_code=400, detail="paitent already exist")
    else:
        #include_computed=True ensures bmi and vedic are saved
        patient_dict = patient.model_dump(exclude=["id"])  # dump normal fields
        patient_dict["id"] = patient.id
        patient_dict["bmi"] = patient.bmi
        patient_dict["vedic"] = patient.vedic

  
        # Save patient data
        data[patient.id] = patient_dict

    return JSONResponse(status_code=201, content="patient created successfully")
