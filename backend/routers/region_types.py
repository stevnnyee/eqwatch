from fastapi import APIRouter
from schemas import RegionTypeCreate
import services.region_types as regiontype_service

router = APIRouter()


@router.get("/")
def list_region_types():
    return regiontype_service.get_all_region_types()


@router.post("/")
def create_region_type(body: RegionTypeCreate):
    return regiontype_service.create_region_type(body)


@router.get("/{type_id}")
def get_region_type(type_id: int):
    return regiontype_service.get_region_type(type_id)


@router.delete("/{type_id}")
def delete_region_type(type_id: int):
    return regiontype_service.delete_region_type(type_id)
