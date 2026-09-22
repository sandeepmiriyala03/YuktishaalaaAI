from fastapi import APIRouter, HTTPException

from models.employee import Employee, EmployeeUpdate
from services.employee_service import EmployeeService

router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)

@router.get("/employees")
def get_employees():
    return EmployeeService.get_employees()


@router.get("/sp")
def get_employees_sp():
    return EmployeeService.get_employees_sp()


@router.get("/{employee_id}")
def get_employee(employee_id: int):
    employee = EmployeeService.get_employee(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.post("")
def create_employee(
    employee: Employee
):
    return EmployeeService.create_employee(
        employee
    )


@router.put("/{employee_id}")
def update_employee(employee_id: int, employee: EmployeeUpdate):
    updated = EmployeeService.update_employee(employee_id, employee)
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee updated"}


@router.delete("/{employee_id}", status_code=204)
def delete_employee(employee_id: int):
    if not EmployeeService.delete_employee(employee_id):
        raise HTTPException(status_code=404, detail="Employee not found")