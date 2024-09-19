import asyncio

import pytest


@pytest.fixture(scope="function", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
