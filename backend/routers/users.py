from fastapi import APIRouter
from schemas import UserCreate
import services.users as user_service

router = APIRouter()


@router.get("/")
def list_users():
    return user_service.get_all_users()


@router.post("/")
def create_user(body: UserCreate):
    return user_service.create_user(body)


@router.get("/{user_id}")
def get_user(user_id: int):
    return user_service.get_user(user_id)


@router.delete("/{user_id}")
def delete_user(user_id: int):
    return user_service.delete_user(user_id)
