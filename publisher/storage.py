"""Local storage functions."""

from redis import Redis

from publisher.settings import app_settings

db_pool: Redis = Redis.from_url(
    app_settings.REDIS_DSN,
    encoding='utf-8',
    decode_responses=True,
)

POSTED_ADS_KEY = 'prague-publisher:posted_ads:id'
TTL_POSTED_ADS = 60 * 60 * 24 * 90  # 3 month  # noqa: WPS432


def mark_as_posted(ads_ids: list[int]) -> int:
    """Mark ads as posted."""
    cnt = 0
    for one_id in ads_ids:
        db_pool.set(f'{POSTED_ADS_KEY}:{one_id}', 1, ex=TTL_POSTED_ADS)
        cnt += 1

    return cnt


def is_not_posted_yet(ads_id: int) -> bool:
    """Check what ads was already posted."""
    is_posted = db_pool.exists(f'{POSTED_ADS_KEY}:{ads_id}')

    return not is_posted
