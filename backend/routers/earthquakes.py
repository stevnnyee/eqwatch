from fastapi import APIRouter
import services.earthquakes as eq_service

router = APIRouter()


@router.get("/")
def list_earthquakes():
    return eq_service.get_all_earthquakes()


@router.get("/{earthquake_id}")
def get_earthquake(earthquake_id: int):
    return eq_service.get_earthquake(earthquake_id)
