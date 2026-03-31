from fastapi import FastAPI
from routers import (
    users,
    earthquakes,
    regions,
    alerts,
    user_regions,
    notification_preferences,
)

app = FastAPI(title="EQWatch API")

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(earthquakes.router, prefix="/earthquakes", tags=["earthquakes"])
app.include_router(regions.router, prefix="/regions", tags=["regions"])
app.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
app.include_router(user_regions.router, prefix="/user-regions", tags=["user_regions"])
app.include_router(notification_preferences.router, prefix="/notification-preferences", tags=["notification_preferences"])


@app.get("/")
def root():
    return {"message": "EQWatch API is running"}
