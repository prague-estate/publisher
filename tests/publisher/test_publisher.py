from collections import Counter

from publisher.publisher import _publisher


async def test_publisher_smoke():
    res = await _publisher(limit=2)

    assert isinstance(res, Counter)
