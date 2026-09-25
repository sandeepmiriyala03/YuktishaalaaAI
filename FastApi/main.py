import fastapi
from pydantic import BaseModel

yukaiApp = fastapi.FastAPI(
    title="Yukai FastAPI",
    version="1.0.0",
    description="This is a sample FastAPI application for user management.",
    docs_url="/docs",
    redoc_url="/redoc",
)

class User(BaseModel):
    name: str
    Age: int | None = None 
    id: int | None = None

# ఇన్-మెమరీ డేటాబేస్ (List)
userDetails = [{"name": "yukai", "Age": 20, "id": 1}]

@yukaiApp.get("/")
def read_root():
    return {"message": "Hello World"}

# Login path
@yukaiApp.get("/login")
async def get_user():
    return {"message": "login successful"}

# Create User Path
@yukaiApp.post("/userCreate")
def create_user(user: User):
    # Pydantic v2 కోసం .model_dump() వాడాలి (.dict() బదులుగా)
    user_data = user.model_dump()
    
    user_data["name"] = user_data["name"].lower()
 
    # లిస్ట్‌లో యాడ్ చేయడం
    userDetails.append(user_data)
       
    return {
        "message": "User created successfully",
        "data": user_data,
        "all_users": userDetails
    }


#get path 

@yukaiApp.get("/get", status_code=200)
async def get_user(user: User):  # User మోడల్‌ని టైప్‌గా ఇవ్వడం
    for user_data in userDetails:
        if user_data["name"] == user.name.lower():
            return {"message": "User found", "data": user_data}
            
    return {"message": "User not found"}



# Post Path
@yukaiApp.post("/post")
async def post_user(user: User):
    print(user.name)
    print(user.Age)
    print(user.id)
    print(userDetails)
    return {"message": "post successful"}