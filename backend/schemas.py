from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class RegionCreate(BaseModel):
    name: str
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float
    type_id: int


class AlertCreate(BaseModel):
    user_id: int
    eq_id: int


class DataSourceCreate(BaseModel):
    name: str
    url: str


class RegionTypeCreate(BaseModel):
    type_name: str


class UserRegionCreate(BaseModel):
    user_id: int
    region_id: int


class NotificationPreferenceCreate(BaseModel):
    user_id: int
    min_magnitude: float
    notify_email: bool
