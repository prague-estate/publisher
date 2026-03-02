"""Estates API client."""
import logging

import aiohttp

from publisher.components.types import Estate
from publisher.settings import app_settings

BASIC_URL = f'{app_settings.API_URL}/v2/estates'

logger = logging.getLogger(__file__)


async def fetch_estates(
    limit: int,
    category: str | None = None,
    without_duplicates: bool = False,
    sliding_window_hours: int | None = None,
) -> list[Estate]:
    """Fetch estates by API."""
    request_params = {
        'limit': limit,
    }
    if category:
        request_params['category'] = category
    if without_duplicates is not None:
        request_params['without_duplicates'] = str(without_duplicates)
    if sliding_window_hours is not None:
        request_params['sliding_window_hours'] = sliding_window_hours

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(app_settings.TIMEOUT)) as session:
        try:
            async with session.get(
                url=BASIC_URL,
                params=request_params,
                headers={'auth-token': app_settings.API_TOKEN},
            ) as resp:
                raw_ads_list = (await resp.json())['estates']

        except Exception as fetch_exc:
            logger.warning('fetch exception {0}'.format(fetch_exc))
            return []
    return [
        Estate(**estate)
        for estate in raw_ads_list
    ]
