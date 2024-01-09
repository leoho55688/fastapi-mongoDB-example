from enum import Enum
from typing import List
from pydantic import MongoDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppEnvTypes(Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"

class AppSettings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes.dev
    debug: bool = True
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    
    title: str = "Backend Practice"
    version: str = "0.0.0"

    database_url: str
    database_name: str
    max_connection_count: int = 5
    min_connection_count: int = 1

    secret_key: SecretStr

    api_prefix: str = "/api"

    jwt_token_prefix: str = "Token"

    allowed_hosts: List[str] = ["*"]

    model_config = SettingsConfigDict(
        validate_assignment=True,
        env_file=".env",
        env_file_encoding="UTF-8"
        )
    
    @property
    def fastapi_kwargs(self) -> None:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version
        }