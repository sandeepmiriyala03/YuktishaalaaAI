from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.employee_controller import router as employee_router
from api.department_controller import router as department_router

app = FastAPI(
    title="YuktishaalaaAI API"
)

# Add your custom production domain right here
origins = [
    "http://localhost:3000",
    "https://yuktishaalaa-ai.vercel.app",
    "https://aksharatantra.miriyala.in"  # <-- Added your exact frontend domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee_router)
app.include_router(department_router)