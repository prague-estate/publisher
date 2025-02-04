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
    PUBLISH_ADS_LIMIT: int = Field(default=1000)

    API_TOKEN: str = Field(default='dev-token')
    API_URL: str = Field(default='http://127.0.0.1:9001')
    REDIS_DSN: str = Field('redis://localhost:6379/1')

    ADMINS: str = ''

    TRIAL_PERIOD_DAYS: int = 14
    PROMO_CODES: dict[str, int] = {
        'vas3k': 31,
        'semrush': 31,
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

    ENABLED_DISTRICTS: list[int] = list(range(1, 22))

    def is_admin(self, user_id: int) -> bool:
        """Check the user is admin or not."""
        return bool(str(user_id) in self.ADMINS.split(';'))


app_settings = AppSettings(
    _env_file=os.path.join(APP_PATH, '.env'),  # type:ignore
)

prices_settings = {
    50: Price(cost=50, days=7, title='Week access'),
    100: Price(cost=100, days=31, title='Month access 🌟'),
    750: Price(cost=750, days=365, title='Year access'),
}
if app_settings.DEBUG:
    prices_settings[1] = Price(
        cost=1,
        days=7,
        title='Test 7-day access',
    )
