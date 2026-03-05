from publisher.channel_publisher import _post_ads_to_channel, _prepare_ads_for_post
from publisher.settings import app_settings


async def test_post_ads_to_channel_smoke(fixture_estate_item):
    res = await _post_ads_to_channel(_prepare_ads_for_post([fixture_estate_item]), app_settings.PUBLISH_CHANNEL_SALE_ID)

    assert res == 1
