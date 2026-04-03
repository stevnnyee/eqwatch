import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_user: str
    db_password: str
    db_name: str = "earthquakes"

    model_config = {"env_file": os.path.join(os.path.dirname(__file__), "..", ".env")}


settings = Settings()
