from pydantic import BaseModel

class Department(BaseModel):
    departmentName: str
    location: str


class DepartmentUpdate(Department):
    pass