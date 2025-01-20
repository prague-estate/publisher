from collections import Counter

from publisher.publisher import publisher


async def test_publisher_smoke():
    res = await publisher(limit=2)

    assert isinstance(res, Counter)
