from fastapi import APIRouter
from schemas import AlertCreate
import services.alerts as alert_service

router = APIRouter()


@router.get("/")
def list_alerts():
    return alert_service.get_all_alerts()


@router.post("/")
def create_alert(body: AlertCreate):
    return alert_service.create_alert(body)


@router.delete("/{alert_id}")
def delete_alert(alert_id: int):
    return alert_service.delete_alert(alert_id)
