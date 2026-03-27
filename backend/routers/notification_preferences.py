from fastapi import APIRouter
from schemas import NotificationPreferenceCreate
import services.notification_preferences as pref_service

router = APIRouter()


@router.get("/{user_id}")
def get_preferences_for_user(user_id: int):
    return pref_service.get_preferences_for_user(user_id)


@router.post("/")
def create_preference(body: NotificationPreferenceCreate):
    return pref_service.create_preference(body)


@router.delete("/{pref_id}")
def delete_preference(pref_id: int):
    return pref_service.delete_preference(pref_id)
