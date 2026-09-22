from fastapi import APIRouter, HTTPException

from models.department import Department, DepartmentUpdate
from services.department_service import DepartmentService

router = APIRouter(
    prefix="/department",
    tags=["Department"]
)


@router.get("/departments")
def get_departments():
    return DepartmentService.get_departments()


@router.get("/{department_id}")
def get_department(department_id: int):
    department = DepartmentService.get_department(department_id)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.post("")
def create_department(
    department: Department
):

    return DepartmentService.create_department(
        department
    )


@router.put("/{department_id}")
def update_department(department_id: int, department: DepartmentUpdate):
    updated = DepartmentService.update_department(department_id, department)
    if not updated:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"message": "Department updated"}


@router.delete("/{department_id}", status_code=204)
def delete_department(department_id: int):
    if not DepartmentService.delete_department(department_id):
        raise HTTPException(status_code=404, detail="Department not found")