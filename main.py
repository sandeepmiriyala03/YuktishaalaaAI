from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# 1. Import RedirectResponse
from fastapi.responses import RedirectResponse

from api.employee_controller import router as employee_router
from api.department_controller import router as department_router

app = FastAPI(
    title="YuktishaalaaAI API"
)

# Allowed production domains
origins = [
    "http://localhost:3000",
    "https://yuktishaalaa-ai.vercel.app",
    "https://aksharatantra.miriyala.in" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Add the root redirect route here
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

app.include_router(employee_router)
app.include_router(department_router)