from publisher.publisher import _post_ads_to_subscriptions
from publisher.components.storage import renew_subscription, update_user_settings


async def test_post_ads_to_subscriptions_subs_not_exists(fixture_estate_item):
    res = await _post_ads_to_subscriptions(
        [fixture_estate_item],
        [],
    )

    assert res == 0


async def test_post_ads_to_subscriptions_subs_not_compatible(fixture_estate_item):
    sub = renew_subscription(user_id=1, days=1)
    update_user_settings(user_id=1, enabled=False)

    res = await _post_ads_to_subscriptions(
        [fixture_estate_item],
        [sub],
    )

    assert res == 0


async def test_post_ads_to_subscriptions_happy_path(fixture_estate_item):
    sub = renew_subscription(user_id=1, days=1)
    update_user_settings(user_id=1)

    res = await _post_ads_to_subscriptions(
        [fixture_estate_item],
        [sub],
    )

    assert res == 1


async def test_post_ads_to_subscriptions_house(fixture_estate_item_house, fixture_estate_item):
    sub = renew_subscription(user_id=1, days=1)
    update_user_settings(user_id=1, property_type='house')

    res = await _post_ads_to_subscriptions(
        [fixture_estate_item_house, fixture_estate_item],
        [sub],
    )

    assert res == 1
