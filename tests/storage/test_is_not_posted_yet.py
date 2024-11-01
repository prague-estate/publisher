from publisher.storage import is_not_posted_yet


async def test_is_not_posted_yet():
    res = await is_not_posted_yet(1)

    assert res is True
