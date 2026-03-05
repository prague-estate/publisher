from publisher.channel_publisher import publish


async def test_publish_smoke():
    res = await publish()

    assert res is None
