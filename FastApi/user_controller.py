from fastapi import APIRouter, HTTPException

from models.user import User
from services.user_service import userService   

router = APIRouter(
    prefix="/users",
    tags=["user"]
)

@router.get("/users")
def get_users():
    return userService.get_users()


@router.get("/{user_id}")
def get_user(user_id: int):
    current_user = userService.get_user(user_id)
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return current_user


@router.post("")
def create_user(
    user: User
):
    return userService.create_user(
        user
    )


@router.put("/{user_id}")
def update_user(user_id: int, user: User):
    updated = userService.update_user(user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated"}


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int):
    if not userService.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")