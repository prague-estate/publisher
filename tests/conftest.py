import asyncio

import pytest

from publisher.storage import mark_as_posted, db_pool


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
async def fixture_empty_posted_ads_id():
    await db_pool.flushdb()
    yield
    await db_pool.flushdb()


@pytest.fixture()
async def fixture_prefilled_posted_ads_id(fixture_empty_posted_ads_id) -> list[int]:
    ads_ids = [1, 2, 3]
    await mark_as_posted(ads_ids)
    yield ads_ids
