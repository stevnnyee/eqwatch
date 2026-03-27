from fastapi import APIRouter
from schemas import RegionCreate
import services.regions as region_service

router = APIRouter()


@router.get("/")
def list_regions():
    return region_service.get_all_regions()


@router.post("/")
def create_region(body: RegionCreate):
    return region_service.create_region(body)


@router.get("/{region_id}")
def get_region(region_id: int):
    return region_service.get_region(region_id)


@router.delete("/{region_id}")
def delete_region(region_id: int):
    return region_service.delete_region(region_id)
