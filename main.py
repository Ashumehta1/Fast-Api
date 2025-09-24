from fastapi import FastAPI,Path
import json

app=FastAPI()

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
    return {"error":"patient not found"}