from publisher.publisher import _publisher
from collections import Counter


async def test_publisher_smoke():
    res = await _publisher()

    assert isinstance(res, Counter)
