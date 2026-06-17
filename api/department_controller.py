from fastapi import APIRouter

from models.department import Department
from services.department_service import DepartmentService

router = APIRouter(
    prefix="/department",
    tags=["Department"]
)

@router.post("")
def create_department(
    department: Department
):

    return DepartmentService.create_department(
        department
    )