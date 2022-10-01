import json
from typing import Any, Dict, Optional

from pydantic import AnyUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    POSTGRES_SSL_MODE: str = "prefer"
    SQLALCHEMY_DATABASE_URI: Optional[AnyUrl]

    CBR_URL: AnyUrl = "https://www.cbr.ru/scripts/XML_daily.asp"

    REDIS_PASSWORD: str
    REDIS_USER: str = "user"
    REDIS_ADDRESS: str
    REDIS_PORT: int = 6379
    REDIS_DB_BACKEND_NUMBER: int = 1
    REDIS_DB_BROKER_NUMBER: int = 0

    CREDENTIALS: str = "app/oath.json"

    TELEGRAM_TOKEN: str
    TELEGRAM_NOTIFICATION_USER_CHAT_ID: int

    CELERY_TIMEZONE: str = "UTC"
    EXCEL_TASK_INTERVAL: str = "*/1 * * * *"
    """Интервал запуска генерации рабочих смен (каждую 1 минуту)"""

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str) and v != "":
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=str(values.get("POSTGRES_PORT")),
            path=f"/{values.get('POSTGRES_DB') or ''}",
            query=f"sslmode={values.get('POSTGRES_SSL_MODE')}",
        )

    @property
    def credentials(self) -> Dict[str, str]:
        with open(self.CREDENTIALS, "r") as f:
            return json.loads(f.read())

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
