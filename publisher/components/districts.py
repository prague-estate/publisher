"""Districts helpers."""
from cachetools import TTLCache
from cachetools_async import cached

from publisher.components.api_client import fetch_districts
from publisher.components.types import District


@cached(cache=TTLCache(maxsize=2048, ttl=30))
async def get_district_names() -> list[str]:
    """Fetch districts and return only names."""
    districts: list[District] = await fetch_districts()
    return sorted([
        district.name
        for district in districts
    ])
