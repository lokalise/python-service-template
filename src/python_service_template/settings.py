import enum
import typing as t

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggingLevel(str, enum.Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggingConfig(BaseModel):
    level: LoggingLevel
    format: t.Literal["JSON", "PLAIN"]


class CoffeeApi(BaseModel):
    host: str


class Settings(BaseSettings):
    host: str
    port: int
    logging: LoggingConfig
    coffee_api: CoffeeApi

    model_config = SettingsConfigDict(
        env_file=(".env.default", ".env"),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )
