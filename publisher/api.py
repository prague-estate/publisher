"""Estates API client."""
import logging

import aiohttp

from publisher.settings import app_settings
from publisher.types import Estate

BASIC_URL = 'http://127.0.0.1:9001/estates/'

logger = logging.getLogger(__file__)


async def fetch_estates(category: str, limit: int) -> list[Estate]:
    """Fetch estates by API."""
    # todo test
    request_params = {
        'limit': limit,
    }
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(app_settings.TIMEOUT)) as session:
        try:
            async with session.get(
                url=f'{BASIC_URL}/{category}',
                params=request_params,
                headers={'auth-token': 'dev-token'},
            ) as resp:
                raw_ads_list = (await resp.json())['estates']

        except Exception as fetch_exc:
            logger.warning('fetch exception {0}'.format(fetch_exc))
            return []
    return [
        Estate(**estate)
        for estate in raw_ads_list
    ]
