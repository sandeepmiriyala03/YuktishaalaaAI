from fastapi import APIRouter

from models.employee import Employee
from services.employee_service import EmployeeService

router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)

@router.get("/employees")
def get_employees():
    return EmployeeService.get_employees()

@router.get("/sp")
def get_employee():
    return EmployeeService.get_employees_sp()

@router.post("")
def create_employee(
    employee: Employee
):
    return EmployeeService.create_employee(
        employee
    )