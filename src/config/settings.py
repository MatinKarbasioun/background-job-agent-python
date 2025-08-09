from functools import lru_cache
from pydantic import SecretStr, AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

from typing_extensions import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent/'.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
    )

    database_url: str = Field(alias='DATABASE_URL')
    task_gateway_url: AnyHttpUrl = Field(alias='TASK_GATEWAY_URL')
    task_gateway_health_check: AnyHttpUrl = Field(alias='TASK_GATEWAY_HEALTH_CHECK')
    task_gateway_api_key: SecretStr = Field(alias='TASK_GATEWAY_API_KEY')
    allowed_hosts: List[str] = Field(alias='ALLOWED_HOSTS', default=["localhost"])


@lru_cache()
def get_settings() -> Settings:
    return Settings()

