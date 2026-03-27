from fastapi import APIRouter
from schemas import UserRegionCreate
import services.user_regions as userregion_service

router = APIRouter()


@router.get("/{user_id}")
def get_regions_for_user(user_id: int):
    return userregion_service.get_regions_for_user(user_id)


@router.post("/")
def add_user_region(body: UserRegionCreate):
    return userregion_service.add_user_region(body)


@router.delete("/{user_id}/{region_id}")
def remove_user_region(user_id: int, region_id: int):
    return userregion_service.remove_user_region(user_id, region_id)
