from publisher.publisher import _post_ads
from publisher.settings import app_settings


async def test_post_ads(fixture_estates_list):
    res = await _post_ads(fixture_estates_list, app_settings.PUBLISH_CHANNEL_SALE_ID)

    assert res == 0
