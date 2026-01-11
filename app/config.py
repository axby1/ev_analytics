# centralized, typed config. No globals scattered everywhere.
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str
    mongo_db: str = "ev_analytics"
    mongo_collection: str = "vehicles"

    class Config:
        env_file = ".env"


settings = Settings()