"""Local storage functions."""

from redis import asyncio as aioredis

from publisher.settings import app_settings

db_pool: aioredis.Redis = aioredis.from_url(
    app_settings.REDIS_DSN,
    encoding='utf-8',
    decode_responses=True,
)

POSTED_ADS_KEY = 'prague-publisher:posted_ads:id'


async def mark_as_posted(ads_ids: list[int]) -> int:
    """Mark ads as posted."""
    # todo impl
    # todo use TTL for auto-cleanup after 3 months
    # todo test
    return 0


async def is_not_posted_yet(ads_id: int) -> bool:
    """Check what ads was already posted."""
    # todo test
    is_posted = await db_pool.exists(f'{POSTED_ADS_KEY}:{ads_id}')

    return not is_posted
