"""Application settings."""
import os

from pydantic import Field
from pydantic_settings import BaseSettings

from publisher.components.types import Price

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
    FETCH_ADS_LIMIT: int = Field(default=500)
    SHOW_ADS_LIMIT: int = Field(default=3)

    API_TOKEN: str = Field(default='dev-token')
    API_URL: str = Field(default='http://127.0.0.1:9001')
    REDIS_DSN: str = Field('redis://localhost:6379/1')

    ADMINS: str = ''

    TRIAL_PERIOD_DAYS: int = 7
    PROMO_CODES: dict[str, int] = {
        'vas3k': 14,
        'semrush': 14,
        'github': 7,
        'landing': 7,
    }

    ENABLED_LAYOUTS: list[str] = [
        'one_kk',
        'one_one',
        'two_kk',
        'two_one',
        'three_kk',
        'three_one',
        'four_kk',
        'four_more',
        'others',
    ]

    ENABLED_DISTRICTS: list[int] = list(range(1, 11))

    def is_admin(self, user_id: int) -> bool:
        """Check the user is admin or not."""
        return bool(str(user_id) in self.ADMINS.split(';'))


app_settings = AppSettings(
    _env_file=os.path.join(APP_PATH, '.env'),  # type:ignore
)

_raw_prices = [
    Price(cost=99, days=7, title='Week access'),  # 45CZK
    Price(cost=299, days=31, title='Month access 🌟'),  # ~125CZK
    Price(cost=1499, days=365, title='Year access'),  # 629CZK
]
prices_settings = {
    price.cost: price
    for price in _raw_prices
}
if app_settings.DEBUG:
    prices_settings[1] = Price(
        cost=1,
        days=7,
        title='Test 7-day access',
    )
