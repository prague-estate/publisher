"""Application settings."""
import os

from pydantic import Field
from pydantic_settings import BaseSettings

from publisher.types import Price

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
    TIMEOUT: int = 35
    PUBLISH_CHANNEL_SALE_ID: int = Field(default=-1002190184244)
    PUBLISH_CHANNEL_LEASE_ID: int = Field(default=-1002199845067)
    PUBLISH_ADS_LIMIT: int = Field(default=100)

    API_TOKEN: str = Field(default='dev-token')
    API_URL: str = Field(default='http://127.0.0.1:9001')
    REDIS_DSN: str = Field('redis://localhost:6379/1')


app_settings = AppSettings(
    _env_file=os.path.join(APP_PATH, '.env'),  # type:ignore
)

prices_settings = {
    50: Price(cost=50, days=7, title='Buy week subscription'),
    150: Price(cost=150, days=31, title='Buy month subscription 🌟 '),
    750: Price(cost=750, days=365, title='Buy year subscription'),
}
if app_settings.DEBUG:
    prices_settings[1] = Price(
        cost=1,
        days=1,
        title='Test 1 day subscription',
    )
