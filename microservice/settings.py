import enum
import os
from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080
UPLOAD_DIRECTORY = f"./media/uploads/"
LOGS_PATH = f"./logs.txt"
TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """
    encrypt_key: str = b'Wk-mIcdQD-y-CwBvJ8V9sEhs4PtcjI90-QLGNu0I9y4='

    host: str = "127.0.0.1"
    port: int = 12315
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO
    users_secret: str = ""

    # Variables for the database
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_pass: str = ""
    db_base: str = ""
    db_echo: bool = False

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )
   
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="MICROSERVICE_",
        env_file_encoding="utf-8",
    )


settings = Settings()