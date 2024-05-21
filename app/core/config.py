import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8',
                                      extra='allow')

    PROJECT_NAME: str = Field(..., alias="PROJECT_NAME")

    REDIS_HOST: str = Field(..., alias="REDIS_HOST")
    REDIS_PORT: str = Field(..., alias="REDIS_PORT")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.REDIS_URL = f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'


settings = Settings()
