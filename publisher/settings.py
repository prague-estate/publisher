"""Application settings."""
import os

from pydantic import AnyUrl, Field, RedisDsn
from pydantic_settings import BaseSettings

APP_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
    ),
)


class AppSettings(BaseSettings, extra='ignore'):
    """Application settings class."""

    DEBUG: bool = Field(default=False)
    BOT_TOKEN: str
    PUBLISH_CHANNEL_SALE_ID: int = Field(default=-1002190184244)
    PUBLISH_CHANNEL_LEASE_ID: int = Field(default=-1002199845067)

    API_TOKEN: str = Field(default='dev-token')
    API_URL: AnyUrl = Field(default='http://127.0.0.1:9001')
    REDIS_DSN: RedisDsn = Field('redis://localhost:6379/1')


app_settings = AppSettings(
    _env_file=os.path.join(APP_PATH, '.env'),  # type:ignore
)
