from fastapi import FastAPI

from api.employee_controller import router as employee_router
from api.department_controller import router as department_router

app = FastAPI(
    title="YuktishaalaaAI API"
)

app.include_router(
    employee_router
)

app.include_router(
    department_router
)