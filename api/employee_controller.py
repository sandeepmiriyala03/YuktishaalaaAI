from fastapi import APIRouter

from models.employee import Employee
from services.employee_service import EmployeeService

router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)

@router.post("")
def create_employee(
    employee: Employee
):

    return EmployeeService.create_employee(
        employee
    )