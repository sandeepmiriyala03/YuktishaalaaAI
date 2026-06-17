from pydantic import BaseModel

class Employee(BaseModel):
    name: str
    salary: int
    age: int
    departmentId: int