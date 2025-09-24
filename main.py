from fastapi import FastAPI
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

