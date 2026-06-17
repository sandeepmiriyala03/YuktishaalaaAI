from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()

API_KEY = "sandeep123"

class Employee(BaseModel):
    id: int
    name: str
    salary: int
    age: int

class department(BaseModel):
    name: str
    location: str
    employees: list[Employee]

@app.post("/employee")
def create_employee(
    employee: Employee,
    x_api_key: str = Header()
):

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    return {
        "message": employee.name + " has been created."
    }


@app.post("/department")
def create_department(
    department: department,
    x_api_key: str = Header()
):

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    return {
        "Message": "Department details"
    }