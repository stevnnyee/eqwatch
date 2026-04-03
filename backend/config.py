from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_user: str
    db_password: str
    db_name: str = "earthquakes"

    model_config = {"env_file": ".env"}


settings = Settings()
