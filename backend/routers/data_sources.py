from fastapi import APIRouter
from schemas import DataSourceCreate
import services.data_sources as datasource_service

router = APIRouter()


@router.get("/")
def list_datasources():
    return datasource_service.get_all_datasources()


@router.post("/")
def create_datasource(body: DataSourceCreate):
    return datasource_service.create_datasource(body)


@router.get("/{source_id}")
def get_datasource(source_id: int):
    return datasource_service.get_datasource(source_id)


@router.delete("/{source_id}")
def delete_datasource(source_id: int):
    return datasource_service.delete_datasource(source_id)
