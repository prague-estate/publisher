from publisher.publisher import _post_ads
from publisher.settings import app_settings
from publisher.storage import is_not_posted_yet


async def test_post_ads_smoke(fixture_estate_item):
    res = await _post_ads([fixture_estate_item], app_settings.PUBLISH_CHANNEL_SALE_ID)

    assert res == 1
    assert is_not_posted_yet(fixture_estate_item.id) is False
